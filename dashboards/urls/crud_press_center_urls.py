# dashboards/urls/crud_press_center_urls.py
from django.urls import path
from ..views import crud_press_center

urlpatterns = [
    # PressCenterPage
    path('page/', crud_press_center.PressCenterPageListView.as_view(), name='presscenterpage_list'),
    path('page/add/', crud_press_center.PressCenterPageCreateView.as_view(), name='presscenterpage_add'),
    path('page/<int:pk>/edit/', crud_press_center.PressCenterPageUpdateView.as_view(), name='presscenterpage_edit'),
    path('page/<int:pk>/delete/', crud_press_center.PressCenterPageDeleteView.as_view(), name='presscenterpage_delete'),

    # PressCenterImage
    path('images/', crud_press_center.PressCenterImageListView.as_view(), name='presscenterimage_list'),
    path('images/add/', crud_press_center.PressCenterImageCreateView.as_view(), name='presscenterimage_add'),
    path('images/<int:pk>/edit/', crud_press_center.PressCenterImageUpdateView.as_view(), name='presscenterimage_edit'),
    path('images/<int:pk>/delete/', crud_press_center.PressCenterImageDeleteView.as_view(), name='presscenterimage_delete'),

    # PublicationRequest
    path('requests/', crud_press_center.PublicationRequestListView.as_view(), name='publicationrequest_list'),
    path('requests/<int:pk>/edit/', crud_press_center.PublicationRequestUpdateView.as_view(), name='publicationrequest_edit'),
    path('requests/<int:pk>/delete/', crud_press_center.PublicationRequestDeleteView.as_view(), name='publicationrequest_delete'),
]