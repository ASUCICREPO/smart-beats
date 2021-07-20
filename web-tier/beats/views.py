from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City
from .utils import init_logger

logger = init_logger(__name__)


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