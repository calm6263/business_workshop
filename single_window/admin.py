from django.contrib import admin
from .models import BasicInfo, FAQ, ServiceRequest, Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'subtitle', 'description']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'description', 'image', 'is_active', 'order')
        }),
        ('Ссылка', {
            'fields': ('link', 'link_text')
        }),
    )

@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']
    fieldsets = (
        ('Контактная информация', {
            'fields': ('address', 'phone', 'email', 'director')
        }),
        ('Документы и структура', {
            'fields': ('position_document', 'position_file', 'department')
        }),
        ('График работы', {
            'fields': ('working_days', 'lunch_break', 'weekend', 'working_description')
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешить только одну запись
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['service', 'question_number', 'question', 'is_active']
    list_filter = ['service', 'is_active']
    list_editable = ['is_active', 'question_number']
    search_fields = ['question', 'answer']
    ordering = ['service', 'question_number']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('service', 'question_number', 'is_active')
        }),
        ('Вопрос и ответ', {
            'fields': ('question', 'answer')
        }),
    )

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'service_type', 'contact_person', 'phone', 'status', 'user', 'created_at']
    list_filter = ['status', 'created_at', 'service_type']
    search_fields = ['request_number', 'contact_person', 'phone', 'email', 'user__username']
    readonly_fields = ['request_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('request_number', 'user', 'service_type', 'format', 'status')
        }),
        ('Контактная информация', {
            'fields': ('contact_person', 'phone', 'email')
        }),
        ('Дополнительная информация', {
            'fields': ('additional_info', 'agreed_to_terms', 'admin_notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )