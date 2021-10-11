import datetime
import pytz
import logging
import os
import shutil
import uuid
from time import sleep

import boto3
import geopandas as gpd
import folium
import pandas as pd
from folium import Choropleth
from django.db.models import Q
from beats.models import Crime, Query

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
AWS_STORAGE_BUCKET_NAME = 'smart-beats-cic'
POLYGON_WISE_COUNT_SHAPEFILE_BUCKET = 'polygon_wise_count_shapefile'


# Logging
def init_logger(name):
    logger = logging.getLogger(name)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename='web_tier.log',
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    return logger


logger = init_logger(__name__)


def delete_file(file_path):
    logger.info(f'Deleting {file_path} after 60 s')
    sleep(60)
    if os.path.exists(file_path):
        os.remove(file_path)


def upload_file_to_s3(filepath, object_name):
    s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME).upload_file(filepath,
                                                            f'{POLYGON_WISE_COUNT_SHAPEFILE_BUCKET}/{object_name}')


def check_if_query_exists(payload):
    priority = ','.join(payload['priority'])
    is_incident = payload['is_incident']
    disposition = ','.join(payload['disposition'])
    beat_creation_method = payload['beat_creation_method']
    cfs_per_beat = payload['cfs_per_beat']
    number_of_beats = payload['number_of_beats']
    start_datetime = payload['start_datetime']
    end_datetime = payload['end_datetime']

    logger.info("Checking if query using following params have been computed before.")
    logger.info("===================================")
    logger.info(f"{priority}, {is_incident}, {disposition}, {beat_creation_method}, {cfs_per_beat}, "
                f"{number_of_beats}, {start_datetime}, {end_datetime}")
    logger.info("===================================")

    base_query = Q(priority=priority) & Q(is_incident=is_incident) & Q(disposition=disposition) & Q(
        beat_creation_method=beat_creation_method) & Q(start_datetime=start_datetime) & Q(end_datetime=end_datetime)

    if cfs_per_beat:
        base_query &= Q(cfs_per_beat=cfs_per_beat)

    if number_of_beats:
        base_query &= Q(number_of_beats=number_of_beats)

    # Only return successful precomputed queries
    query_with_zip_filter = base_query & Q(beat_shapefile_name__endswith='.zip')

    match = Query.objects.filter(query_with_zip_filter).first()
    logger.info(f"Matched Query object: {match}")
    if not match:
        q = Query(priority=priority, is_incident=is_incident, disposition=disposition,
                  beat_creation_method=beat_creation_method, cfs_per_beat=cfs_per_beat, number_of_beats=number_of_beats,
                  start_datetime=start_datetime, end_datetime=end_datetime)
        q.save()

        return False, Query.objects.filter(base_query).first()

    return True, match


def get_filtered_crime_geo_dataframe(payload, city_obj):
    priority_list = payload['priority']
    is_incident = payload['is_incident']
    disposition_types = payload['disposition']

    sd = payload['start_datetime']
    start_datetime = datetime.datetime(sd.year, sd.month, sd.day, sd.hour, sd.minute,
                                       tzinfo=pytz.timezone('US/Arizona'))
    ed = payload['end_datetime']
    end_datetime = datetime.datetime(ed.year, ed.month, ed.day, ed.hour, ed.minute, tzinfo=pytz.timezone('US/Arizona'))

    # Add check for time range to query
    query = Q(timestamp__gte=start_datetime) & Q(timestamp__lte=end_datetime)

    # Add check for Priority info, disposition and incident status to query
    if priority_list:
        query &= Q(priority__in=priority_list)

    if disposition_types:
        query &= Q(disposition__in=disposition_types)

    if is_incident:
        query &= Q(is_incident=is_incident)

    query_res = Crime.objects.filter(query).values()
    logger.info(f"Total rows received: {len(query_res)}")

    if len(query_res) == 0:
        logger.info("Invalid Params. Couldn't generate beats.")
        return None

    # Fixing crime csv file before join
    crime_gdf = gpd.GeoDataFrame(query_res, columns=['priority', 'geometry', 'geometry_wkt'])
    crime_gdf['geometry'] = gpd.GeoSeries.from_wkt(crime_gdf['geometry_wkt'])
    crime_gdf.crs = 'epsg:4326'

    logger.info(f'Filtered crime:\n {crime_gdf.head()}')
    logger.info(f'Crime gdf info: {crime_gdf.dtypes}')

    # Fixing city shapefile before join
    city_polygons = gpd.read_file(city_obj.city_shapefile)
    city_polygons.crs = 'epsg:4326'
    city_polygons = city_polygons[['geometry']]

    logger.info(f"City shapefile:\n {city_polygons.head()}")
    logger.info(f'Crime gdf info: {city_polygons.dtypes}')

    logger.info("Doing a spatial join on crime csv and city shapefile")
    crime_with_city_polygon = gpd.sjoin(crime_gdf, city_polygons, how='inner', op='intersects')

    polygon_wise_crime_counts = pd.DataFrame(crime_with_city_polygon.groupby('index_right').index_right.count())
    polygon_wise_crime_counts = pd.concat([city_polygons, polygon_wise_crime_counts], axis=1)
    polygon_wise_crime_counts = polygon_wise_crime_counts.rename(columns={'index_right': 'count'})
    polygon_wise_crime_counts['count'] = polygon_wise_crime_counts['count'].fillna(0)
    polygon_wise_crime_counts = gpd.GeoDataFrame(polygon_wise_crime_counts)
    logger.info(polygon_wise_crime_counts)

    pwcc_shapefile = ''.join([str(uuid.uuid4().hex[:6]), '_pwcc'])
    polygon_wise_crime_counts.to_file(filename=f"temp/{pwcc_shapefile}", driver='ESRI Shapefile')
    shutil.make_archive(f"temp/{pwcc_shapefile}", 'zip', f"temp/{pwcc_shapefile}")

    upload_file_to_s3(f"temp/{pwcc_shapefile}.zip", f"{pwcc_shapefile}.zip")
    return f"{pwcc_shapefile}.zip"


def create_beats_map(beats_shapefile_url, beat_prefix):
    beats_gpd = gpd.read_file(beats_shapefile_url)
    beats_gpd = beats_gpd[['ZONE_ID', 'geometry', 'count']]

    beats = beats_gpd.dissolve(by='ZONE_ID', aggfunc='sum')
    beats['beat_no'] = beats.index

    beatmap = folium.Map(location=[33.548264, -112.191696], zoom_start=11)

    Choropleth(geo_data=beats,
               data=beats,
               columns=['beat_no', 'count'],
               key_on="feature.properties.beat_no",
               fill_color='YlGnBu',
               legend_name='Calls For Service count'
               ).add_to(beatmap)

    total_beats = beats_gpd['ZONE_ID'].nunique()
    logger.info(f"Total Number of beats: {total_beats}")
    loc = f"Total Number of Beats: {total_beats}"
    title_html = f'''
                 <h4 align="center" style="font-size:16px"><b>{loc}</b></h4>
                 '''
    beatmap.get_root().html.add_child(folium.Element(title_html))

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    tt_overlay = folium.features.GeoJson(
        beats,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['beat_no', 'count'],
            aliases=['Beat No: ', 'Calls for Service count: '],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
        )
    )

    beatmap.add_child(tt_overlay)
    beatmap.keep_in_front(tt_overlay)
    folium.LayerControl().add_to(beatmap)

    beatmap.save(f'beats/templates/beats/{beat_prefix}.html')
