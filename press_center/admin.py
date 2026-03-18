from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.shortcuts import redirect
from .models import PressCenterPage, PressCenterImage, PublicationRequest

class PressCenterImageInline(admin.TabularInline):
    model = PressCenterImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(PressCenterPage)
class PressCenterPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_editable = ['is_active']
    inlines = [PressCenterImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'background_image', 'description', 'is_active', 'publication_rules_file')
        }),
    )

    def has_add_permission(self, request):
        return not PressCenterPage.objects.exists()

    def add_view(self, request, form_url='', extra_context=None):
        if not self.has_add_permission(request):
            self.message_user(request, 'يمكن إنشاء صفحة واحدة فقط للصحافة المركز.', level=messages.ERROR)
            return redirect('admin:press_center_presscenterpage_changelist')
        return super().add_view(request, form_url, extra_context)


@admin.register(PublicationRequest)
class PublicationRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'organization', 'theme', 'contact_person', 'phone', 'email', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['request_number', 'organization', 'theme', 'contact_person', 'phone', 'email']
    readonly_fields = ['request_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Информация о публикации', {
            'fields': ('request_number', 'organization', 'theme', 'desired_dates', 'additional_wishes')
        }),
        ('Контактная информация', {
            'fields': ('contact_person', 'phone', 'email')
        }),
        ('Статус заявки', {
            'fields': ('status',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'in_progress': 'blue',
            'completed': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'