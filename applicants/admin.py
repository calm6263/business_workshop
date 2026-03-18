from django.contrib import admin
from django.utils.html import format_html
from .models import ApplicantsPage, ApplicantDocument, ApplicantApplication, ApplicationMethod, EnrollmentStage

@admin.register(ApplicationMethod)
class ApplicationMethodAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    fields = ['title', 'icon_svg', 'question_svg', 'order', 'is_active']


@admin.register(EnrollmentStage)
class EnrollmentStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active']
    fields = ['name', 'description', 'image', 'order', 'is_active']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border: 1px solid #ddd;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Предпросмотр"


@admin.register(ApplicantsPage)
class ApplicantsPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at',
                    'background_image_preview', 'rocket_image_preview',
                    'conditions_file_link', 'enrollment_conditions_link',
                    'programs_list_link', 'benefits_link',
                    'contract_sample_link', 'useful_links_link',
                    'methods_review_text', 'methods_login_text']
    list_editable = ['is_active']
    readonly_fields = ['background_image_preview', 'rocket_image_preview',
                       'conditions_file_link', 'enrollment_conditions_link',
                       'programs_list_link', 'benefits_link',
                       'contract_sample_link', 'useful_links_link']
    fields = ['title', 'background_image', 'rocket_image',
              'conditions_file', 'enrollment_conditions_file',
              'programs_list_file', 'benefits_file',
              'contract_sample_file', 'useful_links_file',
              'methods_review_text', 'methods_login_text',
              'is_active']

    def has_add_permission(self, request):
        return not ApplicantsPage.objects.exists()

    def background_image_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border: 1px solid #ddd;" />',
                obj.background_image.url
            )
        return "Нет изображения"
    background_image_preview.short_description = 'Фон (предпросмотр)'

    def rocket_image_preview(self, obj):
        if obj.rocket_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border: 1px solid #ddd;" />',
                obj.rocket_image.url
            )
        return "Нет изображения"
    rocket_image_preview.short_description = 'Ракета (предпросмотр)'

    def conditions_file_link(self, obj):
        if obj.conditions_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать</a>', obj.conditions_file.url)
        return "Нет файла"
    conditions_file_link.short_description = "Файл условий приема"

    def enrollment_conditions_link(self, obj):
        if obj.enrollment_conditions_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать условия поступления</a>',
                               obj.enrollment_conditions_file.url)
        return "Нет файла"
    enrollment_conditions_link.short_description = "Условия поступления"

    def programs_list_link(self, obj):
        if obj.programs_list_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать перечень программ</a>',
                               obj.programs_list_file.url)
        return "Нет файла"
    programs_list_link.short_description = "Перечень программ"

    def benefits_link(self, obj):
        if obj.benefits_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать льготы</a>',
                               obj.benefits_file.url)
        return "Нет файла"
    benefits_link.short_description = "Льготы и особые условия"

    def contract_sample_link(self, obj):
        if obj.contract_sample_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать образец договора</a>',
                               obj.contract_sample_file.url)
        return "Нет файла"
    contract_sample_link.short_description = "Образец договора"

    def useful_links_link(self, obj):
        if obj.useful_links_file:
            return format_html('<a href="{}" target="_blank">📄 Скачать полезные ссылки</a>',
                               obj.useful_links_file.url)
        return "Нет файла"
    useful_links_link.short_description = "Полезные ссылки и документы"


@admin.register(ApplicantDocument)
class ApplicantDocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'file_preview']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']

    def file_preview(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">📄 Просмотреть</a>',
                obj.file.url
            )
        return "Нет файла"
    file_preview.short_description = 'Файл'


@admin.register(ApplicantApplication)
class ApplicantApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'contact_person', 'phone', 'email', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['application_number', 'contact_person', 'phone', 'email']
    readonly_fields = ['application_number', 'created_at', 'updated_at']

    actions = ['mark_as_processed', 'mark_as_approved']

    def mark_as_processed(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, f"{queryset.count()} заявок помечены как 'В обработке'")
    mark_as_processed.short_description = "Отметить как 'В обработке'"

    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} заявок одобрены")
    mark_as_approved.short_description = "Одобрить выбранные заявки"

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
            'completed': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'