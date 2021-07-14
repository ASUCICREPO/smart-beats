from django.db import models


class City(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city_shapefile = models.FileField(upload_to='city_shapefiles/')
    beats_shapefile = models.FileField(upload_to='beat_shapefiles/', null=True, blank=True)
    beats_img = models.ImageField(upload_to='city_beats/')
    cfs_chart_img = models.ImageField(upload_to='city_cfs_chart/')
    crime_data = models.FileField(upload_to='city_crime_ds/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city}, {self.state} in {self.country}'

    def delete(self, *args, **kwargs):
        self.city_shapefile.delete()
        self.crime_data.delete()
        super().delete(*args, **kwargs)
