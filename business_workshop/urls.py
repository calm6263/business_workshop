from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views  # استيراد views الخاص بالـ main لاستخدام دوال الأخطاء

urlpatterns = [
    # Админка Django (оставляем доступ только для администраторов системы)
    path('secure-admin-9xA7pL/', admin.site.urls),

    # Приложения
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('applicants/', include('applicants.urls')),
    path('press-center/', include('press_center.urls')),
    path('events/', include('events.urls')),
    path('schedule/', include('schedule.urls')),
    path('projects/', include('projects.urls')),
    path('single-window-services/', include('single_window.urls')),
    path('journal/', include('fta_journal.urls')),
    path('partners/', include('partners.urls')),
    path('research/', include('research.urls')),
    path('departments/', include('departments.urls')),
    path('about-academy/', include('about_academy.urls')),
    path('contacts/', include('contacts.urls')),
    path('coworking/', include('coworking.urls')),
    path('consultations/', include('consultations.urls')),
    path('contact/', include('contact_form.urls')),
    path('dashboard/', include('dashboards.urls')),
    path('education-info/', include('education_info.urls')),
    path('notifications/', include('notifications.urls')),
    path('patents/', include('patents.urls')),
]

admin.site.site_header = ' - Личный портал сотрудника'
admin.site.site_title = ' - Портал'
admin.site.index_title = 'Добро пожаловать в личный портал'

# ============================================
# Обработчики ошибок (Error Handlers)
# ============================================
handler400 = 'main.views.custom_400_view'
handler403 = 'main.views.custom_403_view'
handler404 = 'main.views.custom_404_view'
handler500 = 'main.views.custom_500_view'

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)