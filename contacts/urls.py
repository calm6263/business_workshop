from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('contacts/', views.contacts_page, name='contacts_page'),
]