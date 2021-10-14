import os.path

import requests
import threading

from django.conf import settings as s
from django.shortcuts import render, redirect
from .forms import CityForm, BeatGenerateForm
from .models import City
from . import utils as u
import shutil
import mimetypes
from django.http.response import HttpResponse

logger = u.init_logger(__name__)
url = s.APP_SERVER_URL
AWS_STORAGE_BUCKET_NAME = 'smart-beats-cic'


def home(request):
    cities = City.objects.all()
    return render(request, 'beats/home.html', {'cities': cities})


def upload(request):
    if request.method == 'POST':
        logger.info("Uploading city data")
        form = CityForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            if City.objects.filter(city='Glendale').exists():
                data_row = City.objects.get(city='Glendale')
                logger.info("Previous object exists")
                if data['city_shapefile']:
                    data_row.city_shapefile = data['city_shapefile']
                    data_row.save()
                if data['crime_data']:
                    data_row.crime_data = data['crime_data']
                    data_row.save()
                logger.info("Update complete")
            else:
                form.save()
                logger.info("Upload complete")

            data_row = City.objects.get(city='Glendale')
            key_name = str(data_row.crime_data)
            logger.info(f"Key name + {key_name}")
            u.upload_handler(key_name)
            return redirect('/generate/1')
    else:
        form = CityForm()

    return render(request, 'beats/upload.html', {'form': form})

def download_file(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'example.csv'
    filepath = BASE_DIR + '/beats/static/beats/' + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def generate_beats(request, obj_id=None):
    city_obj = City.objects.get(id=obj_id)
    logger.info(f"city_obj: {city_obj}")
    beat_map_html = None
    polygon_wise_count_shapefile = None

    if request.method == 'POST':
        try:
            form = BeatGenerateForm(request.POST)
            logger.info(f'Uncleaned form data: {form.data}')
            if form.is_valid():
                payload = form.cleaned_data

                # Getting 'is_incident' data from 'type_of_data' radio button
                payload['is_incident'] = payload['type_of_data']

                logger.info(f'Generate beat from data: {payload}')

                query_status, query_obj = u.check_if_query_exists(payload)
                if query_status:
                    logger.info("Requested Query has been generated before")
                    beat_shapefile_name = query_obj.beat_shapefile_name
                else:
                    logger.info("First time Query")

                    polygon_wise_count_shapefile = u.get_filtered_crime_geo_dataframe(
                        payload, city_obj)

                    if not polygon_wise_count_shapefile:
                        logger.info(
                            "Couldn't generate beats due to invalid request. Redirecting to error page")
                        return render(request, 'beats/error.html')

                    payload['polygon_wise_count_shapefile'] = polygon_wise_count_shapefile

                    response = requests.post(url=url, data=payload)

                    status = response.status_code
                    beat_shapefile_name = response.text

                    logger.info(
                        f'Http response: {status}, Beat name: {beat_shapefile_name}')

                    logger.info(
                        "Updating Query object with beat shapefile name")
                    query_obj.beat_shapefile_name = beat_shapefile_name
                    query_obj.save()

                logger.info(f'Beat name: {beat_shapefile_name}')
                beat_url = f'zip+s3://{AWS_STORAGE_BUCKET_NAME}/beat_shapefiles/{beat_shapefile_name}'

                beat_prefix = beat_shapefile_name.split('.')[0]
                logger.info(
                    f'beat_url: {beat_url}, beat_prefix: {beat_prefix}')
                u.create_beats_map(beat_url, beat_prefix)

                beat_map_html = f'beats/{beat_prefix}.html'
                return render(request, beat_map_html)
            else:
                logger.info(f"Invalid form data: {form.cleaned_data}")
                logger.info('Well... the form turned out to be invalid')
        finally:
            if polygon_wise_count_shapefile:
                pwcc_dir = polygon_wise_count_shapefile.split('.')[0]

                t1 = threading.Thread(target=u.delete_file, args=(
                    f'temp/{polygon_wise_count_shapefile}',))
                t1.start()

                if os.path.exists(f'temp/{pwcc_dir}'):
                    logger.info(f'Deleting pwcc_dir {pwcc_dir}')
                    shutil.rmtree(f'temp/{pwcc_dir}')

            if beat_map_html:
                t2 = threading.Thread(target=u.delete_file, args=(
                    f'beats/templates/{beat_map_html}',))
                t2.start()
    else:
        form = BeatGenerateForm()

    return render(request, 'beats/generate_beats.html', {'form': form})


def beats_list(request):
    cities = City.objects.all()
    return render(request, 'beats/beats_list.html', {
        'cities': cities
    })
