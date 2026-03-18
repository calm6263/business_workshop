from django.urls import path
from . import views

app_name = 'education_info'

urlpatterns = [
    path('', views.education_info, name='education_info'),
]