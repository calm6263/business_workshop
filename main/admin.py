from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Page, Application, Document, EducationalProgram,
    Slide, License
)

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25
    save_on_top = True
    list_max_show_all = 100

@admin.register(Slide)
class SlideAdmin(BaseAdmin):
    list_display = ['title', 'slide_type', 'order', 'is_active', 'preview_image', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['slide_type', 'is_active', 'created_at']
    search_fields = ['title', 'caption']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slide_type', 'caption', 'order', 'is_active'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Медиа контент', {
            'fields': ('image', 'video'),
            'description': 'Выберите изображение или видео в зависимости от типа слайда',
            'classes': ('wide',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Превью'

@admin.register(Application)
class ApplicationAdmin(BaseAdmin):
    list_display = ['application_number', 'contact_person', 'phone', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['application_number', 'contact_person', 'phone']
    readonly_fields = ['application_number', 'created_at', 'updated_at']
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
            'completed': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

@admin.register(License)
class LicenseAdmin(BaseAdmin):
    list_display = ['title', 'order', 'is_active', 'preview_file', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title']
    fieldsets = (
        ('Информация о лицензии', {
            'fields': ('title', 'file', 'order', 'is_active'),
            'classes': ('wide', 'extrapretty')
        }),
    )
    
    def preview_file(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Посмотреть файл</a>', obj.file.url)
        return "—"
    preview_file.short_description = 'Файл'

admin.site.register(Page)
admin.site.register(Document)
admin.site.register(EducationalProgram)