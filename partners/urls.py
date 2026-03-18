from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.partners_list, name='partners_list'),
    path('<int:pk>/', views.partner_detail, name='partner_detail'),
    # يمكن إزالة هذا المسار أو الاحتفاظ به للتوافق
    path('application/', views.partnership_application, name='partnership_application'),
]