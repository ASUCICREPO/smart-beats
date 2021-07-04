from django.shortcuts import render, redirect
from beats.custom_storage import ShapefileStorage, CrimeDataStorage
from .forms import CityForm
from .models import City


def home(request):
    return render(request, 'beats/home.html')


def upload(request):
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)

        if form.is_valid():
            shape_file = request.FILES['shape_file']
            crime_data = request.FILES['crime_data']

            shape_file_bucket = ShapefileStorage()
            crime_data_bucket = CrimeDataStorage()

            shape_file_bucket.save(shape_file.name, shape_file)
            crime_data_bucket.save(crime_data.name, crime_data)

            form.save()
            return redirect('beats_list')
    else:
        form = CityForm()

    return render(request, 'beats/upload.html', {'form': form})


def upload_shapefile(request):
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        media_storage = ShapefileStorage()
        # Get updated name of file in case of same-name upload
        name = media_storage.save(uploaded_file.name, uploaded_file)
        context['url'] = media_storage.url(name)

    return render(request, 'beats/upload.html', context)


def upload_crime_data(request):
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        media_storage = CrimeDataStorage()
        print(media_storage.bucket_name)

        # Get updated name of file in case of same-name upload
        name = media_storage.save(uploaded_file.name, uploaded_file)
        context['url'] = media_storage.url(name)

    return render(request, 'beats/upload.html', context)


def beats_list(request):
    cities = City.objects.all()
    return render(request, 'beats/beats_list.html', {
        'cities': cities
    })
