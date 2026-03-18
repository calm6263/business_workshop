from django.urls import path
from . import views

app_name = 'patents'

urlpatterns = [
    path('', views.patents_list, name='patents_list'),
]