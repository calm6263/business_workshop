from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.departments_list, name='departments_list'),
    path('<int:pk>/', views.department_detail, name='department_detail'),
    path('archive/', views.archive_programs_list, name='archive_programs_list'),  # صفحة الأرشيف
]