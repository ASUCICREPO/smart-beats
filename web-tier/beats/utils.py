import logging
import os
from time import sleep

import boto3
import geopandas as gpd
import folium
from folium import Choropleth

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
AWS_STORAGE_BUCKET_NAME = 'smart-beats-cic'


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


def delete_file(file_path):
    print(f'Deleting {file_path} after 10 s')
    sleep(10)
    if os.path.exists(file_path):
        os.remove(file_path)


def create_beats_map(beats_shapefile_url, beat_prefix):
    # beats_gpd = gpd.read_file(city_obj.city_shapefile.url)
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

    # beatmap.save(f'{city_obj.city}_beats_map.html')

    beatmap.save(f'beats/templates/beats/{beat_prefix}.html')
