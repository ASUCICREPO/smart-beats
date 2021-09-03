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

    DISPOSITION_CHOICES = [
        ('initial', 'Select'),
        (1, 'Field Interview (1)'),
        (2, 'False Alarm (2)'),
        (3, 'Unable to locate (3)'),
        (5, 'Assist Fire Department (5)'),
        (6, 'Report (6)'),
        (9, 'Contact made (9)'),
    ]

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES)
    disposition_type = forms.ChoiceField(choices=DISPOSITION_CHOICES)
    cfs_per_beat = forms.IntegerField(label='Calls for Service per Beat', required=False)
    number_of_beats = forms.DecimalField(required=False)
    start_datetime = forms.DateTimeField(widget=forms.NumberInput(attrs={'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(widget=forms.NumberInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Crime
        fields = (
            'priority', 'is_incident', 'disposition_type', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats',
            'start_datetime', 'end_datetime')

    class Media:
        js = ('beats/js/main.js',)
