from django.shortcuts import render
from django.views.generic import TemplateView
from beats.custom_storage import TestDataStorage, ShapefileStorage, CrimeDataStorage


class Home(TemplateView):
    template_name = 'beats/home.html'


class Upload(TemplateView):
    template_name = 'beats/upload.html'


def upload(request):
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        media_storage = TestDataStorage()
        # Get updated name of file in case of same-name upload
        name = media_storage.save(uploaded_file.name, uploaded_file)
        context['url'] = media_storage.url(name)

    return render(request, 'beats/upload.html', context)


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
