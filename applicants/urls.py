from django.urls import path
from . import views

urlpatterns = [
    path('applicants/', views.applicants_page, name='applicants'),
    path('applicants/foreign/', views.foreign_applicants_view, name='foreign_applicants'),
    path('applicants/submit/', views.submit_application, name='submit_application'),
    path('applicants/search/', views.search_application, name='search_application'),
]