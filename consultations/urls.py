from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('', views.consultation_form, name='consultation_form'),
    path('success/', views.success, name='success'),
]