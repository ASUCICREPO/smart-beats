from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('upload/test', views.upload, name='upload-test'),
    path('upload/shapefile', views.upload_shapefile, name='upload-shapefile'),
    path('upload/crimedata', views.upload_crime_data, name='upload-crime-data'),
]
