from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('beats/', views.beats_list, name='beats_list'),
    path('beats/upload', views.coming_soon, name='upload'),
]