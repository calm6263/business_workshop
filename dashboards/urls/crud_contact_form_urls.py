# dashboards/urls/crud_contact_form_urls.py
from django.urls import path
from ..views import crud_contact_form

urlpatterns = [
    path('messages/', crud_contact_form.ContactMessageListView.as_view(), name='contactmessage_list'),
    path('messages/<int:pk>/edit/', crud_contact_form.ContactMessageUpdateView.as_view(), name='contactmessage_edit'),
    path('messages/<int:pk>/delete/', crud_contact_form.ContactMessageDeleteView.as_view(), name='contactmessage_delete'),
]