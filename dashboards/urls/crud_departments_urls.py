# dashboards/urls/crud_departments_urls.py
from django.urls import path
from ..views import crud_departments

urlpatterns = [
    # Department
    path('departments/', crud_departments.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', crud_departments.DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', crud_departments.DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', crud_departments.DepartmentDeleteView.as_view(), name='department_delete'),

    # HeroImage
    path('hero-images/', crud_departments.HeroImageListView.as_view(), name='heroimage_list'),
    path('hero-images/add/', crud_departments.HeroImageCreateView.as_view(), name='heroimage_add'),
    path('hero-images/<int:pk>/edit/', crud_departments.HeroImageUpdateView.as_view(), name='heroimage_edit'),
    path('hero-images/<int:pk>/delete/', crud_departments.HeroImageDeleteView.as_view(), name='heroimage_delete'),
]