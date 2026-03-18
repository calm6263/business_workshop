# urls.py
from django.urls import path
from . import views

app_name = 'coworking'

urlpatterns = [
    path('', views.coworking_home, name='coworking_home'),
]