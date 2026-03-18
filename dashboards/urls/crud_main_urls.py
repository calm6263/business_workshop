# dashboards/urls/crud_main_urls.py
from django.urls import path
from ..views import crud_main

urlpatterns = [
    # Slide
    path('slides/', crud_main.SlideListView.as_view(), name='slide_list'),
    path('slides/add/', crud_main.SlideCreateView.as_view(), name='slide_add'),
    path('slides/<int:pk>/edit/', crud_main.SlideUpdateView.as_view(), name='slide_edit'),
    path('slides/<int:pk>/delete/', crud_main.SlideDeleteView.as_view(), name='slide_delete'),

    # License
    path('licenses/', crud_main.LicenseListView.as_view(), name='license_list'),
    path('licenses/add/', crud_main.LicenseCreateView.as_view(), name='license_add'),
    path('licenses/<int:pk>/edit/', crud_main.LicenseUpdateView.as_view(), name='license_edit'),
    path('licenses/<int:pk>/delete/', crud_main.LicenseDeleteView.as_view(), name='license_delete'),
]