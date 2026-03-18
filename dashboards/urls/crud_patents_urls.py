# dashboards/urls/crud_patents_urls.py
from django.urls import path
from ..views import crud_patents

urlpatterns = [
    path('', crud_patents.PatentImageListView.as_view(), name='patentimage_list'),
    path('add/', crud_patents.PatentImageCreateView.as_view(), name='patentimage_add'),
    path('<int:pk>/edit/', crud_patents.PatentImageUpdateView.as_view(), name='patentimage_edit'),
    path('<int:pk>/delete/', crud_patents.PatentImageDeleteView.as_view(), name='patentimage_delete'),
]