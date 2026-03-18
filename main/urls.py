from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.index, name='index'),
    
    # الصفحات
    path('about/', views.page_detail, {'slug': 'about'}, name='about'),
    path('contact/', views.page_detail, {'slug': 'contact'}, name='contact'),
    # تم نقل مسار contacts إلى تطبيق contacts المنفصل
    path('pages/<slug:slug>/', views.page_detail, name='page_detail'),
    
    # المركز الإعلامي
    path('news/', include('news.urls')),
    
    # تطبيق الاتصالات المنفصل
    path('contacts/', include('contacts.urls')),
    
   
    
    # الفريق
    path('staff/', include('staff.urls')),
    
    # المعلومات التعليمية - التطبيق الجديد
    path('education-info/', include('education_info.urls')),
    
    # صفحة تحت التطوير - مهم للبطاقات
    path('under-construction/<str:page_name>/', views.under_construction, name='under_construction'),
]