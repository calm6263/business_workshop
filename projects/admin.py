from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectCategory, Project, ProjectMember, ProjectSlide, ProjectPartner, ContactRequest, ProjectProposal, ProjectGallery, ProjectJoinRequest

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 3
    fields = ('title', 'image', 'description', 'order', 'is_active')
    verbose_name = "Изображение галереи"
    verbose_name_plural = "Галерея изображений"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type_badge', 'status_badge', 'start_date', 'is_featured', 'is_active']
    list_filter = ['project_type', 'status', 'is_featured', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'sidebar_title']
    list_editable = ['is_featured', 'is_active']
    inlines = [ProjectGalleryInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'project_type', 'category', 'status', 'is_featured', 'is_active')
        }),
        ('Содержание', {
            'fields': ('sidebar_title', 'description', 'short_description', 'results', 'image', 'description_image', 'presentation_file')
        }),
        ('Даты и бюджет', {
            'fields': ('start_date', 'end_date', 'budget', 'participants_count')
        }),
        ('Порядок', {
            'fields': ('order',)
        }),
    )
    
    def project_type_badge(self, obj):
        colors = {
            'government': 'blue',
            'corporate': 'green',
            'grants': 'purple',
            'contests': 'orange',
            'youth': 'teal',
            'social': 'pink',
            'targeted': 'brown',
            'patents': 'indigo',
            'conferences': 'red'
        }
        color = colors.get(obj.project_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_project_type_display()
        )
    project_type_badge.short_description = 'Тип проекта'
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'completed': 'blue',
            'planned': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'role_badge', 'organization', 'is_active']
    list_filter = ['role', 'is_active', 'project']
    search_fields = ['name', 'organization']
    
    def role_badge(self, obj):
        colors = {
            'leader': 'red',
            'member': 'blue',
            'consultant': 'green',
            'partner': 'purple'
        }
        color = colors.get(obj.role, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Роль'

@admin.register(ProjectPartner)
class ProjectPartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'preview_logo', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'project']
    search_fields = ['name', 'project__title']
    
    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.logo.url
            )
        return "-"
    preview_logo.short_description = 'Логотип'

@admin.register(ProjectSlide)
class ProjectSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview_image', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "-"
    preview_image.short_description = 'Превью'

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at', 'project']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_processed']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Информация о запросе', {
            'fields': ('project', 'name', 'email', 'message', 'created_at', 'is_processed')
        }),
    )

@admin.register(ProjectProposal)
class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'title', 'full_name', 'email', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['unique_id', 'title', 'full_name', 'email']
    readonly_fields = ['unique_id', 'created_at']
    list_editable = []
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('unique_id', 'title', 'description', 'status')
        }),
        ('Контактная информация', {
            'fields': ('full_name', 'email', 'phone', 'organization')
        }),
        ('Дополнительная информация', {
            'fields': ('budget', 'duration', 'created_at')
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'reviewed': 'blue',
            'accepted': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

@admin.register(ProjectGallery)
class ProjectGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview_image', 'project', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'project']
    search_fields = ['title', 'description']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.image.url
            )
        return "-"
    preview_image.short_description = 'Предпросмотр'

@admin.register(ProjectJoinRequest)
class ProjectJoinRequestAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'project', 'person_type', 'status_badge', 'created_at']
    list_filter = ['status', 'person_type', 'created_at', 'project']
    search_fields = ['unique_id', 'project__title', 'full_name_individual', 'full_name_legal', 'email_individual', 'email_legal']
    readonly_fields = ['unique_id', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('unique_id', 'project', 'person_type', 'status', 'created_at')
        }),
        ('Данные физического лица', {
            'fields': ('full_name_individual', 'phone_individual', 'email_individual', 
                      'address_individual', 'comments_individual'),
            'classes': ('collapse',)
        }),
        ('Данные юридического лица', {
            'fields': ('full_name_legal', 'phone_legal', 'email_legal', 'company_name',
                      'inn', 'kpp', 'legal_address', 'comments_legal'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'reviewed': 'blue',
            'accepted': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'