# dashboards/urls/__init__.py
from django.urls import path, include
from ..views import dashboard

app_name = 'dashboards'

urlpatterns = [
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('crud/', include('dashboards.urls.crud_urls')),   # هذا السطر مهم
    path('applicants/', include('dashboards.urls.crud_applicants_urls')),
    path('consultations/', include('dashboards.urls.crud_consultations_urls')),
    path('contacts/', include('dashboards.urls.crud_contacts_urls')),
    path('departments/', include('dashboards.urls.crud_departments_urls')),
    path('events/', include('dashboards.urls.crud_events_urls')),
    path('fta-journal/', include('dashboards.urls.crud_fta_journal_urls')),
    path('news/', include('dashboards.urls.crud_news_urls')),
    path('partners/', include('dashboards.urls.crud_partners_urls')),
    path('press-center/', include('dashboards.urls.crud_press_center_urls')),
    path('projects/', include('dashboards.urls.crud_projects_urls')),
    path('schedule/', include('dashboards.urls.crud_schedule_urls')),
    path('research/', include('dashboards.urls.crud_research_urls')),
    path('single-window/', include('dashboards.urls.crud_single_window_urls')),
    path('staff/', include('dashboards.urls.crud_staff_urls')),
    path('main/', include('dashboards.urls.crud_main_urls')),
    path('contact-form/', include('dashboards.urls.crud_contact_form_urls')),
    path('patents/', include('dashboards.urls.crud_patents_urls')),
]