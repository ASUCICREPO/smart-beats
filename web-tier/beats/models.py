from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.gis.db import models as spatial_models


class City(models.Model):
    city = models.CharField(default='Glendale', max_length=255)
    state = models.CharField(default='Arizona', max_length=255)
    country = models.CharField(default='USA', max_length=255)
    city_shapefile = models.FileField(upload_to='city_shapefiles/', null=True, blank=True)
    crime_data = models.FileField(upload_to='city_crime_ds/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.city_shapefile.delete()
        self.crime_data.delete()
        super().delete(*args, **kwargs)


class Crime(models.Model):
    PRIORITY_CHOICES = ((i, i) for i in range(1, 10))
    DISPOSITION_CHOICES = ((1, '1 - Field Interview'),
                           (2, '2 - False Alarm'),
                           (3, '3 - Unable to locate'),
                           (5, '5 - Assist Fire Department'),
                           (6, '6 - Report'),
                           (9, '9 - Contact made'),)

    event_number = models.CharField(max_length=256)
    priority = MultiSelectField(choices=PRIORITY_CHOICES)
    address = models.CharField(max_length=256)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lon = models.DecimalField(max_digits=5, decimal_places=2)
    geometry = spatial_models.PointField()
    is_incident = models.BooleanField()
    geometry_wkt = models.CharField(max_length=100)
    timestamp = models.DateTimeField(null=True, blank=True)
    disposition = MultiSelectField(choices=DISPOSITION_CHOICES)

    def __str__(self):
        return f"{self.event_number}"


class Query(models.Model):
    priority = models.CharField(max_length=100)
    disposition = models.CharField(max_length=100)
    beat_creation_method = models.CharField(max_length=100)
    cfs_per_beat = models.IntegerField(null=True, blank=True)
    number_of_beats = models.IntegerField(null=True, blank=True)
    start_datetime = models.CharField(max_length=100)
    end_datetime = models.CharField(max_length=100)
    is_incident = models.BooleanField()
    beat_shapefile_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.priority}; {self.disposition};{self.beat_creation_method};{self.cfs_per_beat};" \
               f"{self.number_of_beats};{self.start_datetime};{self.end_datetime};{self.is_incident};" \
               f"{self.beat_shapefile_name}"


