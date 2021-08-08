from django import forms

from .models import City, Crime


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city', 'state', 'country', 'city_shapefile', 'crime_data')


class BeatGenerateForm(forms.ModelForm):
    BEAT_CREATION_CHOICES = [
        ('ATTRIBUTE_TARGET', 'Calls for Service'),
        ('NUMBER_OF_ZONES', 'Number of Beats')
    ]
    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES,
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    cfs_per_beat = forms.IntegerField(label='Calls for Service per Beat', required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    number_of_beats = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Crime
        fields = ('priority', 'is_incident', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats')
