from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('beats_list/', views.beats_list, name='beats_list'),
    path('generate/<int:obj_id>/', views.generate_beats, name='generate_beats'),
    path('upload/', views.upload, name='upload'),
    path('beats_interactive_map/', views.beat_interactive_map,
         name='beats_interactive'),
    path('beats/city_map/<int:obj_id>/', views.city_map, name='city_map'),
]
