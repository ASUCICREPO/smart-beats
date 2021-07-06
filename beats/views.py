from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City


def home(request):
    return render(request, 'beats/home.html')


def upload(request):
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('beats_list')
    else:
        form = CityForm()

    return render(request, 'beats/upload.html', {'form': form})


def beats_list(request):
    cities = City.objects.all()
    return render(request, 'beats/beats_list.html', {
        'cities': cities
    })
