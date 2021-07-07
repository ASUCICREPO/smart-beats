from django.db import models


class City(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    shape_file = models.FileField(upload_to='city_shapefiles/')
    crime_data = models.FileField(upload_to='city_crime_ds/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city}, {self.state} in {self.country}'

    def delete(self, *args, **kwargs):
        self.shape_file.delete()
        self.crime_data.delete()
        super().delete(*args, **kwargs)
