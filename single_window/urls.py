 
from django.urls import path
from . import views

app_name = 'single_window'

urlpatterns = [
    path('', views.single_window_services, name='single_window_services'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('submit-request/', views.submit_service_request, name='submit_service_request'),
    path('my-requests/', views.my_service_requests, name='my_requests'),
]
 