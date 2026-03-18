from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_form_view, name='contact_form'),
    path('partial/', views.contact_form_partial, name='contact_form_partial'),
]