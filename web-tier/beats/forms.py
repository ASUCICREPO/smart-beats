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

    INCIDENT_CHOICES = [
        ('True', 'Incident data only'),
        ('False', 'Calls-For-Service data')
    ]

    # priority_choice = forms.ModelMultipleChoiceField(
    #     queryset=Crime.objects.order_by().values_list('priority', flat=True).distinct())

    beat_creation_method = forms.ChoiceField(choices=BEAT_CREATION_CHOICES, widget=forms.Select(
        attrs={'class': 'field-margins form-control'}))
    cfs_per_beat = forms.IntegerField(label='Calls for Service per Beat', required=False,
                                      widget=forms.NumberInput(attrs={'class': 'field-margins form-control'}))
    number_of_beats = forms.DecimalField(required=False,
                                         widget=forms.NumberInput(attrs={'class': 'field-margins form-control'}))
    start_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'class': 'field-margins form-control', 'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(
        widget=forms.NumberInput(attrs={'class': 'field-margins form-control', 'type': 'datetime-local'}))
    type_of_data = forms.CharField(label='Specify type of data to display',
                                   widget=forms.RadioSelect(choices=INCIDENT_CHOICES))

    class Meta:
        model = Crime
        fields = (
            'priority', 'disposition', 'beat_creation_method', 'cfs_per_beat', 'number_of_beats',
            'start_datetime', 'end_datetime', 'type_of_data')

    class Media:
        js = ('beats/js/main.js',)
