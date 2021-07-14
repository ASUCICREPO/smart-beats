from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('beats/', views.beats_list, name='beats_list'),
    path('beats/upload', views.coming_soon, name='upload'),
    path('beats/beats_interactive_map', views.beat_interactive_map, name='beats_interactive'),
    path('beats/city_map/<int:obj_id>/', views.city_map, name='city_map'),
]
