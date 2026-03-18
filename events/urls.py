# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_page, name='events'),
    path('api/<int:pk>/', views.event_detail_api, name='event_detail_api'),  # جعله أولاً
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/register/', views.event_registration, name='event_registration'),
    path('interesting-programs/<slug:slug>/', views.interesting_program_detail, name='interesting_program_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/search/', views.search_events_api, name='search_events_api'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<slug:slug>/', views.album_detail, name='events_album_detail'),
    
]