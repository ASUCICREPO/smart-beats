# Generated by Django 3.2.4 on 2021-07-20 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0002_city_beats_shapefile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='beats_img',
        ),
        migrations.RemoveField(
            model_name='city',
            name='cfs_chart_img',
        ),
        migrations.AddField(
            model_name='city',
            name='polygon_wise_count_shapefile',
            field=models.FileField(blank=True, null=True, upload_to='polygon_wise_count_shapefile/'),
        ),
    ]
