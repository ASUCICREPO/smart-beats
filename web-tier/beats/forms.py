from django import forms

from .models import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city', 'state', 'country', 'city_shapefile', 'crime_data')


class BeatGenerateForm(forms.Form):
    BEAT_CREATION_CHOICES = [
        ('ATTRIBUTE_TARGET', 'Calls for Service'),
        ('NUMBER_ZONES_AND_ATTRIBUTE', 'Calls for Service & Number of Beats'),
        ('NUMBER_OF_ZONES', 'Number of Beats')]

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    cfs_per_beat = forms.DecimalField(label='CFS per Beat', required=False,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_of_beats = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
