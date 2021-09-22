from django import forms
from .models import City, Crime


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_shapefile', 'crime_data')

    def __init__(self, *args, **kwargs) -> None:
        super(CityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'drop-zone__input'


class BeatGenerateForm(forms.ModelForm):
    BEAT_CREATION_CHOICES = [
        ('initial', "Choose criteria"),
        ('ATTRIBUTE_TARGET', 'Calls for Service'),
        ('NUMBER_ZONES_AND_ATTRIBUTE', 'Number of Beats')
    ]

    DISPOSITION_CHOICES = [
        ('initial', 'Select'),
        (1, '1 - Field Interview'),
        (2, '2 - False Alarm'),
        (3, '3 - Unable to locate'),
        (5, '5 - Assist Fire Department'),
        (6, '6 - Report'),
        (9, '9 - Contact made'),
    ]

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES, widget=forms.Select(
        attrs={'class': 'field-margins form-control'}))
    disposition_type = forms.ChoiceField(choices=DISPOSITION_CHOICES,
                                         widget=forms.Select(attrs={'class': 'field-margins form-control'}))
    cfs_per_beat = forms.IntegerField(label='Calls for Service per Beat', required=False,
                                      widget=forms.NumberInput(attrs={'class': 'field-margins form-control'}))
    number_of_beats = forms.DecimalField(required=False,
                                         widget=forms.NumberInput(attrs={'class': 'field-margins form-control'}))
    start_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'class': 'field-margins form-control', 'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'class': 'field-margins form-control', 'type': 'datetime-local'}))

    class Meta:
        model = Crime
        fields = (
            'priority', 'disposition_type', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats',
            'start_datetime', 'end_datetime', 'is_incident')

    class Media:
        js = ('beats/js/main.js',)
