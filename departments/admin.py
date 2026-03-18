from django.contrib import admin
from .models import Department, HeroImage

class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'is_active', 'order', 'created_at']
    list_filter = ['page', 'is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']
    ordering = ['order', 'page']
    
    fieldsets = (
        ('Настройки страницы', {
            'fields': ('page', 'is_active', 'order')
        }),
        ('Содержимое героя', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Изображение и ссылки', {
            'fields': ('image', 'link_text', 'link')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_program_type_display', 'programs_count', 'is_active', 'order', 'created_at']
    list_filter = ['program_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'programs_count']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'program_type', 'description')
        }),
        ('Изображение и настройки', {
            'fields': ('image', 'order', 'is_active')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def programs_count(self, obj):
        return obj.programs_count
    programs_count.short_description = 'Количество программ'
    
    def get_program_type_display(self, obj):
        return obj.get_program_type_display()
    get_program_type_display.short_description = 'Тип программы'
    get_program_type_display.admin_order_field = 'program_type'


admin.site.register(HeroImage, HeroImageAdmin)
admin.site.register(Department, DepartmentAdmin)