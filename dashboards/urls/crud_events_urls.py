# dashboards/urls/crud_events_urls.py
from django.urls import path
from ..views import crud_events

urlpatterns = [
    # Event
    path('events/', crud_events.EventListView.as_view(), name='event_list'),
    path('events/add/', crud_events.EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/edit/', crud_events.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', crud_events.EventDeleteView.as_view(), name='event_delete'),

    # EventRegistration
    path('registrations/', crud_events.EventRegistrationListView.as_view(), name='eventregistration_list'),
    path('registrations/<int:pk>/edit/', crud_events.EventRegistrationUpdateView.as_view(), name='eventregistration_edit'),
    path('registrations/<int:pk>/delete/', crud_events.EventRegistrationDeleteView.as_view(), name='eventregistration_delete'),

    # InterestingProgram
    path('interesting-programs/', crud_events.InterestingProgramListView.as_view(), name='interestingprogram_list'),
    path('interesting-programs/add/', crud_events.InterestingProgramCreateView.as_view(), name='interestingprogram_add'),
    path('interesting-programs/<int:pk>/edit/', crud_events.InterestingProgramUpdateView.as_view(), name='interestingprogram_edit'),
    path('interesting-programs/<int:pk>/delete/', crud_events.InterestingProgramDeleteView.as_view(), name='interestingprogram_delete'),

    # NewsletterSubscription
    path('newsletter/', crud_events.NewsletterSubscriptionListView.as_view(), name='newslattersubscription_list'),
    path('newsletter/<int:pk>/edit/', crud_events.NewsletterSubscriptionUpdateView.as_view(), name='newslattersubscription_edit'),
    path('newsletter/<int:pk>/delete/', crud_events.NewsletterSubscriptionDeleteView.as_view(), name='newslattersubscription_delete'),

    # PageSettings (для мероприятий и галереи)
    path('page-settings/', crud_events.PageSettingsListView.as_view(), name='pagesettings_list'),
    path('page-settings/add/', crud_events.PageSettingsCreateView.as_view(), name='pagesettings_add'),
    path('page-settings/<int:pk>/edit/', crud_events.PageSettingsUpdateView.as_view(), name='pagesettings_edit'),
    path('page-settings/<int:pk>/delete/', crud_events.PageSettingsDeleteView.as_view(), name='pagesettings_delete'),

    # Album
    path('albums/', crud_events.AlbumListView.as_view(), name='album_list'),
    path('albums/add/', crud_events.AlbumCreateView.as_view(), name='album_add'),
    path('albums/<int:pk>/edit/', crud_events.AlbumUpdateView.as_view(), name='album_edit'),
    path('albums/<int:pk>/delete/', crud_events.AlbumDeleteView.as_view(), name='album_delete'),

    # Photo
    path('photos/', crud_events.PhotoListView.as_view(), name='photo_list'),
    path('photos/add/', crud_events.PhotoCreateView.as_view(), name='photo_add'),
    path('photos/<int:pk>/edit/', crud_events.PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/<int:pk>/delete/', crud_events.PhotoDeleteView.as_view(), name='photo_delete'),
]