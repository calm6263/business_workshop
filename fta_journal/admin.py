from django.contrib import admin
from django.utils.html import format_html
from .models import JournalIssue, SliderImage, SectionSettings, IssuePage

class IssuePageInline(admin.TabularInline):
    model = IssuePage
    extra = 5
    fields = ['image', 'page_number', 'order']
    verbose_name = "Страница"
    verbose_name_plural = "Страницы выпуска"

class JournalIssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'is_published', 'show_in_best', 'show_in_new', 'order', 'cover_preview']
    list_filter = ['is_published', 'publication_date', 'show_in_best', 'show_in_new']
    search_fields = ['title', 'description']
    list_editable = ['is_published', 'show_in_best', 'show_in_new', 'order']
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'description', 'cover_image', 'cover_preview']
        }),
        ('Настройки отображения', {
            'fields': [
                'show_in_best', 'best_order',
                'show_in_new', 'new_order',
                'is_published', 'order'
            ]
        }),
        ('Файлы и даты', {
            'fields': ['publication_date', 'pdf_file']
        }),
    ]
    readonly_fields = ['cover_preview']
    inlines = [IssuePageInline]
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="100" height="140" />', obj.cover_image.url)
        return "Нет изображения обложки"
    cover_preview.short_description = "Предпросмотр обложки"

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'carousel_type', 'order', 'is_active', 'created_at']
    list_editable = ['carousel_type', 'order', 'is_active']
    list_filter = ['carousel_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "Нет изображения. "
    image_preview.short_description = "Предварительный просмотр"

class SectionSettingsAdmin(admin.ModelAdmin):
    list_display = ['best_section_title', 'new_section_title', 'early_section_title']
    
    def has_add_permission(self, request):
        return SectionSettings.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        if SectionSettings.objects.count() == 0:
            SectionSettings.load()
        return super().changelist_view(request, extra_context)

admin.site.register(JournalIssue, JournalIssueAdmin)
admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(SectionSettings, SectionSettingsAdmin)