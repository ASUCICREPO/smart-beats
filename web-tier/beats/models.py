from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.gis.db import models as spatial_models


class City(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city_shapefile = models.FileField(upload_to='city_shapefiles/')
    polygon_wise_count_shapefile = models.FileField(upload_to='polygon_wise_count_shapefile/', null=True, blank=True)
    beats_shapefile = models.FileField(upload_to='beat_shapefiles/', null=True, blank=True)
    crime_data = models.FileField(upload_to='city_crime_ds/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city}, {self.state} in {self.country}'

    def delete(self, *args, **kwargs):
        self.city_shapefile.delete()
        self.polygon_wise_count_shapefile.delete()
        self.beats_shapefile.delete()
        self.crime_data.delete()
        super().delete(*args, **kwargs)


class Crime(models.Model):
    PRIORITY_CHOICES = ((i, i) for i in range(1, 10))

    event_number = models.CharField(max_length=256)
    priority = MultiSelectField(choices=PRIORITY_CHOICES)
    address = models.CharField(max_length=256)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lon = models.DecimalField(max_digits=5, decimal_places=2)
    geometry = spatial_models.PointField()
    is_incident = models.BooleanField()
    geometry_wkt = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.event_number}"
