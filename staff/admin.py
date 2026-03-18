from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, TeacherProgram, PageHero

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25
    save_on_top = True
    list_max_show_all = 100

@admin.register(TeamMember)
class TeamMemberAdmin(BaseAdmin):
    list_display = [
        'name', 
        'member_type_badge', 
        'position', 
        'email', 
        'phone', 
        'order', 
        'is_active', 
        'preview_image',
        'display_departments'
    ]
    list_editable = ['order', 'is_active']
    list_filter = ['member_type', 'is_active', 'created_at', 'departments']
    search_fields = ['name', 'position', 'description', 'email', 'phone']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'member_type', 'position', 'description')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        # تم إزالة القسم الإضافي (qualifications, experience)
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
    
    def member_type_badge(self, obj):
        colors = {
            'teacher': 'blue',
            'staff': 'green',
            'educational_council': 'purple'
        }
        color = colors.get(obj.member_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_member_type_display()
        )
    member_type_badge.short_description = 'Тип'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Фото'
    
    def display_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()[:3]])
    display_departments.short_description = 'Отделения'

@admin.register(TeacherProgram)
class TeacherProgramAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'program', 'role', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'role', 'created_at']
    search_fields = ['teacher__name', 'program__title', 'role']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher', 'program')

@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ['page_display', 'preview_image', 'title', 'is_active', 'updated_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'page']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('Информация о странице', {
            'fields': ('page', 'is_active')
        }),
        ('Содержимое героя', {
            'fields': ('title', 'subtitle', 'image')
        }),
    )
    
    def page_display(self, obj):
        return obj.get_page_display()
    page_display.short_description = 'Страница'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border-radius: 5px;" />', 
                obj.image.url
            )
        return "—"
    preview_image.short_description = 'Предпросмотр изображения'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['page']
        return []