from django.urls import path
from . import views

app_name = 'press_center'

urlpatterns = [
    path('', views.press_center, name='press_center'),
    # تم إزالة مسار التفاصيل القديم
    path('submit-request/', views.submit_publication_request, name='submit_publication_request'),
]