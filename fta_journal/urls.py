from django.urls import path
from . import views

app_name = 'fta_journal'

urlpatterns = [
    path('', views.journal_home, name='journal_home'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('early/', views.early_issues, name='early_issues'),  # صفحة جميع الإصدارات المبكرة
]