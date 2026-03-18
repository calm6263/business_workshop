# admin.py
from django.contrib import admin
from django.utils.html import format_html, escape
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import ConsultationRequest, HeroSlide, FAQ, SuccessPageImage

def staff_or_superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and (u.is_staff or u.is_superuser)
    )(view_func)
    return decorated_view_func

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id_display', 
        'contact_email', 
        'direction_display', 
        'date', 
        'time', 
        'contact_phone', 
        'is_processed', 
        'created_at'
    ]
    list_filter = ['direction', 'is_processed', 'created_at']
    search_fields = ['request_id', 'contact_email', 'contact_phone', 'additional_wishes']
    list_editable = ['is_processed']
    readonly_fields = ['request_id', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_module_permission(self, request):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_processed=False)
    
    def request_id_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; font-weight: bold; color: #7F1726;">{}</span>',
            escape(str(obj.request_id)[:8].upper())
        )
    request_id_display.short_description = 'Номер заявки'
    request_id_display.admin_order_field = 'request_id'
    
    def direction_display(self, obj):
        return escape(obj.get_direction_display())
    direction_display.short_description = 'Направление'
    
    def contact_email(self, obj):
        return escape(obj.contact_email)
    contact_email.short_description = 'E-mail'
    
    def contact_phone(self, obj):
        return escape(obj.contact_phone)
    contact_phone.short_description = 'Телефон'
    
    def additional_wishes_display(self, obj):
        return escape(obj.additional_wishes[:50] + '...' if len(obj.additional_wishes) > 50 else obj.additional_wishes)
    additional_wishes_display.short_description = 'Дополнительные пожелания'
    
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('request_id', 'created_at')
        }),
        ('Контактная информация', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Детали консультации', {
            'fields': ('direction', 'date', 'time')
        }),
        ('Дополнительно', {
            'fields': ('additional_wishes', 'agreed_to_terms')
        }),
        ('Статус', {
            'fields': ('is_processed',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['preview_image', 'title_display', 'subtitle_display', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    
    def has_module_permission(self, request):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" alt="{}" />',
                obj.image.url,
                escape(obj.title or 'Слайд')
            )
        return "Нет изображения"
    preview_image.short_description = 'Предпросмотр'
    
    def title_display(self, obj):
        return escape(obj.title or 'Без названия')
    title_display.short_description = 'Заголовок'
    
    def subtitle_display(self, obj):
        return escape(obj.subtitle or 'Без подзаголовка')
    subtitle_display.short_description = 'Подзаголовок'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_display', 'answer_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    
    def has_module_permission(self, request):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_active and (request.user.is_staff or request.user.is_superuser)
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def question_display(self, obj):
        return escape(obj.question[:100] + '...' if len(obj.question) > 100 else obj.question)
    question_display.short_description = 'Вопрос'
    
    def answer_preview(self, obj):
        return escape(obj.answer[:150] + '...' if len(obj.answer) > 150 else obj.answer)
    answer_preview.short_description = 'Ответ'


@admin.register(SuccessPageImage)
class SuccessPageImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'alt_text', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "Нет изображения"
    thumbnail.short_description = 'Миниатюра'