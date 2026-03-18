from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = [
        ('Информация о сообщении', {
            'fields': ['name', 'email', 'message', 'is_robot', 'is_read']
        }),
        ('Дата', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]

admin.site.register(ContactMessage, ContactMessageAdmin)