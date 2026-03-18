# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # API
    path('api/unread/', views.api_unread_notifications, name='api_unread'),
    path('api/mark-read/<int:notification_id>/', views.api_mark_read, name='api_mark_read'),
    path('api/mark-all-read/', views.api_mark_all_read, name='api_mark_all_read'),

    # Новые API для архивации/удаления
    path('api/archive/<int:notification_id>/', views.api_archive, name='api_archive'),
    path('api/unarchive/<int:notification_id>/', views.api_unarchive, name='api_unarchive'),
    path('api/delete/<int:notification_id>/', views.api_delete, name='api_delete'),
    path('api/archive-all-read/', views.api_archive_all_read, name='api_archive_all_read'),
    path('api/delete-all-archived/', views.api_delete_all_archived, name='api_delete_all_archived'),

    # Страницы
    path('', views.NotificationListView.as_view(), name='list'),
    path('activity-log/', views.ActivityLogListView.as_view(), name='activity_log'),
]