import requests
import threading

from django.shortcuts import render, redirect
from .forms import CityForm, BeatGenerateForm
from .models import City
from . import utils as u

logger = u.init_logger(__name__)
url = "http://ec2-100-26-151-201.compute-1.amazonaws.com:5000"
AWS_STORAGE_BUCKET_NAME = 'smart-beats-cic'


def home(request):
    cities = City.objects.all()
    return render(request, 'beats/home.html', {'cities': cities})


def upload(request):
    if request.method == 'POST':
        logger.info("Uploading city data")
        form = CityForm(request.POST, request.FILES)

        if City.objects.filter(city='Glendale').exists():
            if form.is_valid():
                data = form.cleaned_data
                # logger.info(f"City: {data['city']}, {data['state']} in {data['country']}")
                if data['city_shapefile']:
                    form.save(update_fields=['city_shapefile'])
                if data['crime_data']:
                    form.save(update_fields=['crime_data'])
                logger.info("Upload complete")
                return redirect('/generate/1')
        else:

            if form.is_valid():
                data = form.cleaned_data
                # logger.info(f"City: {data['city']}, {data['state']} in {data['country']}")

                form.save()
                logger.info("Upload complete")
                return redirect('/generate/1')
    else:
        form = CityForm()

    return render(request, 'beats/upload.html', {'form': form})


def generate_beats(request, obj_id=None):
    city_obj = City.objects.get(id=obj_id)
    logger.info(f"city_obj: {city_obj}")
    beat_map_html = None

    if request.method == 'POST':
        try:
            form = BeatGenerateForm(request.POST)
            logger.info(f'Uncleaned form data: {form.data}')
            if form.is_valid():
                payload = form.cleaned_data
                logger.info(f'Generate beat from data: {payload}')

                polygon_wise_count_shapefile = u.get_filtered_crime_geo_dataframe(
                    payload, city_obj)
                payload['polygon_wise_count_shapefile'] = polygon_wise_count_shapefile

                response = requests.post(url=url, data=payload)

                status = response.status_code
                beat_name = response.text
                logger.info(f'Http response: {status}, Beat name: {beat_name}')

                beat_url = f'zip+s3://{AWS_STORAGE_BUCKET_NAME}/beat_shapefiles/{beat_name}'

                beat_prefix = beat_name.split('.')[0]
                logger.info(
                    f'beat_url: {beat_url}, beat_prefix: {beat_prefix}')
                u.create_beats_map(beat_url, beat_prefix)

                beat_map_html = f'beats/{beat_prefix}.html'
                return render(request, beat_map_html)
            else:
                logger.info('Well... the form turned out to be invalid')
        finally:
            if beat_map_html:
                t = threading.Thread(target=u.delete_file, args=(
                    f'beats/templates/{beat_map_html}',))
                t.start()
    else:
        form = BeatGenerateForm()

    return render(request, 'beats/generate_beats.html', {'form': form})


def beats_list(request):
    cities = City.objects.all()
    return render(request, 'beats/beats_list.html', {
        'cities': cities
    })

