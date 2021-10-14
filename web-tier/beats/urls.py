from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('beats_list/', views.beats_list, name='beats_list'),
    path('generate/<int:obj_id>/', views.generate_beats, name='generate_beats'),
    path('upload/', views.upload, name='upload'),
    path('download/', views.download_file, name='download_file'),
]
