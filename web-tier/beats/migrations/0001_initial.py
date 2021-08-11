# Generated by Django 3.2.4 on 2021-08-10 03:43

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city_shapefile', models.FileField(upload_to='city_shapefiles/')),
                ('polygon_wise_count_shapefile', models.FileField(blank=True, null=True, upload_to='polygon_wise_count_shapefile/')),
                ('beats_shapefile', models.FileField(blank=True, null=True, upload_to='beat_shapefiles/')),
                ('crime_data', models.FileField(upload_to='city_crime_ds/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_number', models.CharField(max_length=256)),
                ('priority', multiselectfield.db.fields.MultiSelectField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], max_length=17)),
                ('address', models.CharField(max_length=256)),
                ('lat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lon', models.DecimalField(decimal_places=2, max_digits=5)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('is_incident', models.BooleanField()),
                ('geometry_wkt', models.CharField(max_length=100)),
            ],
        ),
    ]
