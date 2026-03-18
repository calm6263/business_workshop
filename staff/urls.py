from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('teachers-and-staff/', views.teachers_and_staff, name='teachers_and_staff'),
    path('member/<int:pk>/detail/', views.team_member_detail, name='team_member_detail'),
]