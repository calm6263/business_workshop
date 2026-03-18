from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ResearchCategory, Research, ResearchTag, ResearchHero,
    Conference, ConferenceRegistration, YouthCouncilMember,
    YouthCouncilDepartment
)

@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ['title', 'research_type', 'category', 'publication_date', 'is_featured', 'is_active', 'views_count']
    list_filter = ['research_type', 'category', 'publication_date', 'is_featured', 'is_active']
    search_fields = ['title', 'description', 'author']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'research_type', 'category', 'description', 'short_description')
        }),
        ('Медиа и файлы', {
            'fields': ('image', 'file')
        }),
        ('Дополнительно', {
            'fields': ('author', 'publication_date', 'is_featured', 'is_active')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ResearchTag)
class ResearchTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ResearchHero)
class ResearchHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_editable = ['is_active']
    fields = ['title', 'background_image', 'brochure', 'is_active']

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'conference_type', 'start_date', 'end_date', 'location', 'entrance_fee', 'is_active', 'views_count']
    list_filter = ['conference_type', 'start_date', 'is_active']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'conference_type', 'description', 'short_description', 'entrance_fee')
        }),
        ('Медиа и даты', {
            'fields': ('image', 'file', 'start_date', 'end_date', 'location', 'registration_link')
        }),
        ('Контакты и организаторы', {
            'fields': ('contact_person', 'contact_phone', 'contact_email', 'organizers')
        }),
        ('Видео-инструкция', {
            'fields': ('video', 'video_title'),
            'description': 'Короткое видео о том, как добраться до места.'
        }),
        ('Статус и статистика', {
            'fields': ('is_active', 'views_count', 'created_at', 'updated_at')
        }),
    )

@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'conference', 'phone', 'email', 'created_at']
    list_filter = ['conference', 'created_at']
    search_fields = ['full_name', 'phone', 'email', 'registration_number']
    readonly_fields = ['registration_number', 'created_at']

# ===== تسجيل نماذج مجلس الشباب =====
@admin.register(YouthCouncilDepartment)
class YouthCouncilDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'member_count']
    list_editable = ['order', 'is_active']
    search_fields = ['name']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Количество членов'

@admin.register(YouthCouncilMember)
class YouthCouncilMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active', 'preview_image', 'display_departments']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'departments']
    search_fields = ['name', 'position', 'description', 'email', 'phone']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'position', 'description')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Отделения', {
            'fields': ('departments',),
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('wide',)
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
    )
    filter_horizontal = ['departments']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Фото'

    def display_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()[:3]])
    display_departments.short_description = 'Отделения'