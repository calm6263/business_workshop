from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/contact/', views.contact_request, name='contact_request'),
    path('submit-proposal/', views.submit_project_proposal, name='submit_proposal'),
    path('join-request/', views.submit_join_request, name='submit_join_request'),
    
]