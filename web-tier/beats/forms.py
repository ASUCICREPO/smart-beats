from django import forms

from .models import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city', 'state', 'country', 'city_shapefile', 'crime_data')


class BeatGenerateForm(forms.ModelForm):
    BEAT_CREATION_CHOICES = [
        ('ATTRIBUTE_TARGET', 'Calls for Service'),
        ('NUMBER_ZONES_AND_ATTRIBUTE', 'Calls for Service & Number of Beats'),
        ('NUMBER_OF_ZONES', 'Number of Beats')]

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES)
    cfs_per_beat = forms.DecimalField()
    number_of_beats = forms.DecimalField()
