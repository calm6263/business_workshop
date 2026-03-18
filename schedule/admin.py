# schedule/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ScheduleProgram, CurriculumModule, CurriculumDocument, ProgramApplication, ScheduleSliderImage, CalendarSliderImage

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25
    save_on_top = True
    list_max_show_all = 100

class CurriculumModuleInline(admin.TabularInline):
    model = CurriculumModule
    extra = 1
    fields = ('title', 'description', 'order')
    ordering = ('order',)

class CurriculumDocumentInline(admin.TabularInline):
    model = CurriculumDocument
    extra = 1
    fields = ('title', 'document_type', 'file', 'description', 'order', 'is_active')
    ordering = ('order',)

class ScheduleProgramAdmin(BaseAdmin):
    list_display = ['title', 'department', 'program_type_badge', 'certification_badge', 'format_badge', 
                    'start_date', 'end_date', 'duration_hours', 'cost', 'enrollment_status_badge', 
                    'postponed_date', 'is_active', 'order']   # добавлено postponed_date
    list_editable = ['is_active', 'order']
    list_filter = ['department', 'program_type', 'certification_type', 'format', 'start_date', 
                   'end_date', 'is_active', 'enrollment_status']
    search_fields = ['title', 'detailed_description', 'admission_requirements']
    date_hierarchy = 'start_date'
    prepopulated_fields = {'slug': ('title',)}
    
    inlines = [CurriculumModuleInline, CurriculumDocumentInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'department', 'program_type', 'certification_type', 'format')
        }),
        ('Описания', {
            'fields': (
                'detailed_description',
                'schedule_description',
                'admission_requirements',
                'target_audience',
            )
        }),
        ('Даты и продолжительность', {
            'fields': ('start_date', 'end_date', 'duration', 'duration_hours')
        }),
        ('Стоимость и набор', {
            'fields': ('cost', 'enrollment_status', 'postponed_date')   # ← добавлено postponed_date
        }),
        ('Документы и расписание', {
            'fields': ('schedule_document', 'admission_form_document')
        }),
        ('Медиа', {
            'fields': ('image', 'side_image', 'diploma_image_1', 'diploma_image_2')
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def program_type_badge(self, obj):
        colors = {
            'professional_retraining': 'blue',
            'qualification_upgrade': 'green',
            'seminar': 'purple',
            'training': 'orange',
            'other': 'gray',
        }
        color = colors.get(obj.program_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_program_type_display()
        )
    program_type_badge.short_description = 'Тип программы'
    
    def format_badge(self, obj):
        colors = {
            'offline': '#052946',
            'blended': '#7F1726',
            'correspondence': '#37556A',
            'online': '#17a2b8',
        }
        color = colors.get(obj.format, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_format_display()
        )
    format_badge.short_description = 'Формат'
    
    def certification_badge(self, obj):
        colors = {
            'certified': '#28a745',
            'diploma': '#ffc107',
            'attestation': '#17a2b8',
            'none': '#6c757d'
        }
        color = colors.get(obj.certification_type, 'gray')
        display_text = obj.get_certification_type_display()
        if obj.certification_type != 'none':
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
                color, display_text
            )
        return '-'
    certification_badge.short_description = 'Тип сертификации'
    
    def enrollment_status_badge(self, obj):
        colors = {
            'open': '#28a745',
            'closed': '#dc3545',
            'upcoming': '#17a2b8',
            'archive': '#6c757d',
            'on_request': '#ffc107',
            'postponed': '#e83e8c',   # розовый
        }
        color = colors.get(obj.enrollment_status, '#6c757d')
        
        # Отображаем дату, если статус postponed и дата указана
        if obj.enrollment_status == 'postponed' and obj.postponed_date:
            display_text = f"Перенесен на {obj.postponed_date.strftime('%d.%m.%Y')}"
        else:
            display_text = obj.get_enrollment_status_display()
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, display_text
        )
    enrollment_status_badge.short_description = 'Статус набора'
    
    def has_custom_audience(self, obj):
        return bool(obj.target_audience)
    has_custom_audience.boolean = True
    has_custom_audience.short_description = 'Своя аудитория?'

admin.site.register(ScheduleProgram, ScheduleProgramAdmin)

@admin.register(CurriculumModule)
class CurriculumModuleAdmin(BaseAdmin):
    list_display = ['title', 'program', 'order']
    list_filter = ['program']
    search_fields = ['title', 'description']
    list_editable = ['order']

@admin.register(CurriculumDocument)
class CurriculumDocumentAdmin(BaseAdmin):
    list_display = ['title', 'program', 'document_type', 'order', 'is_active']
    list_filter = ['program', 'document_type', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    
    def document_type_badge(self, obj):
        colors = {
            'word': '#2b579a',
            'excel': '#217346',
            'pdf': '#f40f02',
            'other': '#6c757d'
        }
        color = colors.get(obj.document_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_document_type_display()
        )
    document_type_badge.short_description = 'Тип документа'

@admin.register(ProgramApplication)
class ProgramApplicationAdmin(BaseAdmin):
    list_display = ['application_number', 'contact_name', 'program', 'phone', 'email', 'status', 'created_at']
    list_filter = ['program', 'status', 'created_at']
    search_fields = ['application_number', 'contact_name', 'phone', 'email']
    readonly_fields = ['application_number', 'created_at']
    list_editable = ['status']
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

@admin.register(ScheduleSliderImage)
class ScheduleSliderImageAdmin(BaseAdmin):
    list_display = ['title', 'subtitle', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Изображение и ссылка', {
            'fields': ('image', 'link', 'link_text')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'

@admin.register(CalendarSliderImage)
class CalendarSliderImageAdmin(BaseAdmin):
    list_display = ['title', 'subtitle', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Изображение и ссылка', {
            'fields': ('image', 'link', 'link_text')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'