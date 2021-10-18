from django.db import models
from multiselectfield import MultiSelectField
from django.conf import settings as s


class City(models.Model):
    city = models.CharField(default=s.CITY, max_length=255)
    state = models.CharField(default=s.STATE, max_length=255)
    country = models.CharField(default=s.COUNTRY, max_length=255)
    city_shapefile = models.FileField(upload_to=f'{s.S3_CITY_SHAPEFILES_DIR}/', null=True, blank=True)
    crime_data = models.FileField(upload_to=f'{s.S3_CITY_CRIME_DS_DIR}/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.city_shapefile.delete()
        self.crime_data.delete()
        super().delete(*args, **kwargs)


class Crime(models.Model):
    event_number = models.CharField(max_length=256)
    priority = MultiSelectField(choices=s.PRIORITY_CHOICES)
    address = models.CharField(max_length=512)
    is_incident = models.BooleanField()
    geometry_wkt = models.CharField(max_length=100)
    timestamp = models.DateTimeField(null=True, blank=True)
    disposition = MultiSelectField(choices=s.DISPOSITION_CHOICES)

    def __str__(self):
        return f"{self.priority};{self.disposition};{self.is_incident};{self.address};{self.geometry_wkt};" \
               f"{self.timestamp}"


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
