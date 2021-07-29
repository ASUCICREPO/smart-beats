from django.shortcuts import render, redirect
from .forms import CityForm, BeatGenerateForm
from .models import City
from . import utils as u

import requests
import threading

logger = u.init_logger(__name__)
url = "http://ec2-54-210-194-250.compute-1.amazonaws.com:5000"
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
            logger.info(f"City: {data['city']}, {data['state']} in {data['country']}")

            form.save()
            logger.info("Upload complete")
            return redirect('beats_list')
    else:
        form = CityForm()

    return render(request, 'beats/upload.html', {'form': form})


def generate_beats(request):
    beat_map_html = None

    if request.method == 'POST':
        try:
            form = BeatGenerateForm(request.POST)
            if form.is_valid():
                payload = form.cleaned_data
                print(f'Generate beat from data: {payload}')

                response = requests.post(url=url, data=payload)

                status = response.status_code
                beat_name = response.text
                print(f'Http response: {status}, Beat name: {beat_name}')

                beat_url = f'zip+s3://{AWS_STORAGE_BUCKET_NAME}/beat_shapefiles/{beat_name}'

                beat_prefix = beat_name.split('.')[0]
                print(f'beat_url: {beat_url}, beat_prefix: {beat_prefix}')
                u.create_beats_map(beat_url, beat_prefix)

                beat_map_html = f'beats/{beat_prefix}.html'
                return render(request, beat_map_html)
        finally:
            if beat_map_html:
                t = threading.Thread(target=u.delete_file, args=(f'beats/templates/{beat_map_html}',))
                t.start()
    else:
        form = BeatGenerateForm()

    return render(request, 'beats/generate_beats.html', {'form': form})


def beats_list(request):
    cities = City.objects.all()
    return render(request, 'beats/beats_list.html', {
        'cities': cities
    })


def coming_soon(request):
    return render(request, 'beats/coming_soon.html')


def beat_interactive_map(request):
    return render(request, 'beats/glendale_beats_map.html')


def city_map(request, obj_id=None):
    city_obj = City.objects.get(id=obj_id)
    if city_obj.city != 'Glendale':
        return render(request, 'beats/city_map.html', {'city_obj': city_obj})

    return render(request, 'beats/glendale_beats_map.html')
