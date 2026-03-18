from django.contrib import admin
from .models import ContactSection, OrganizationInfo, SocialMedia, ContactPageSettings, ContactHero

@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'section_type', 'phone', 'email', 'order', 'is_active']
    list_filter = ['section_type', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'department_name', 'phone', 'email']
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'section_type', 'department_name', 'description', 'order', 'is_active']
        }),
        ('Контактная информация', {
            'fields': ['phone', 'email', 'additional_phones', 'additional_emails']
        }),
        ('Дополнительная информация', {
            'fields': ['address', 'work_hours']
        }),
    ]

@admin.register(OrganizationInfo)
class OrganizationInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'general_phone', 'general_email']
    
    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not OrganizationInfo.objects.exists()

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'url']

@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'show_breadcrumbs', 'show_organization_info']
    
    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not ContactPageSettings.objects.exists()

@admin.register(ContactHero)
class ContactHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'subtitle', 'description', 'image']
        }),
        ('Настройки отображения', {
            'fields': ['show_breadcrumb', 'is_active']
        }),
    ]
    readonly_fields = ['created_at', 'updated_at']