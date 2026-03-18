# dashboards/urls.py
from django.urls import path, include
from .views import DashboardView  # الآن يشير إلى DashboardView من views/__init__.py

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('crud/', include('dashboards.urls.crud_urls')),
]