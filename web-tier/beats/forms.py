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

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES)
    beat_creation_method.widget.attrs.update(
        {'class': 'field-margins form-control'})
    disposition_type = forms.ChoiceField(choices=DISPOSITION_CHOICES)
    disposition_type.widget.attrs.update(
        {'class': 'field-margins form-control'})
    cfs_per_beat = forms.IntegerField(
        label='Calls for Service per Beat', required=False)
    cfs_per_beat.widget.attrs.update({'class': 'field-margins form-control'})
    number_of_beats = forms.DecimalField(required=False)
    number_of_beats.widget.attrs.update(
        {'class': 'field-margins form-control'})
    start_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'type': 'datetime-local'}))
    start_datetime.widget.attrs.update({'class': 'field-margins form-control'})
    end_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'type': 'datetime-local'}))
    end_datetime.widget.attrs.update({'class': 'field-margins form-control'})

    class Meta:
        model = Crime
        fields = (
            'priority', 'disposition_type', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats',
            'start_datetime', 'end_datetime', 'is_incident')

    class Media:
        js = ('beats/js/main.js',)
