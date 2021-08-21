from django import forms

from .models import City, Crime


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city', 'state', 'country', 'city_shapefile', 'crime_data')


class BeatGenerateForm(forms.ModelForm):
    BEAT_CREATION_CHOICES = [
        ('initial', "Choose criteria"),
        ('ATTRIBUTE_TARGET', 'Calls for Service'),
        ('NUMBER_ZONES_AND_ATTRIBUTE', 'Number of Beats')
    ]
    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES)
    cfs_per_beat = forms.IntegerField(label='Calls for Service per Beat', required=False)
    number_of_beats = forms.DecimalField(required=False)
    start_datetime = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_datetime = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Crime
        fields = (
            'priority', 'is_incident', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats', 'start_datetime',
            'end_datetime')

    class Media:
        js = ('beats/js/main.js',)
