from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_page, name='schedule_page'),
    path('program/<slug:slug>/', views.program_detail, name='program_detail'),
    path('program/<slug:slug>/apply/', views.submit_application, name='submit_application'),
    path('calendar/', views.calendar_view, name='calendar'),
    # المسار الرئيسي لتحميل PDF
    path('download-calendar-pdf/', views.download_calendar_pdf, name='download_calendar_pdf'),
    # مسار النسخة المبسطة (بديل)
    path('download-calendar-pdf-simple/', views.download_calendar_pdf_simple, name='download_calendar_pdf_simple'),
]