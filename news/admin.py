from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from .models import News, Category, NewsPageHero, Subscriber

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish_date', 'is_active', 'preview_image', 'short_content']
    list_filter = ['category', 'publish_date', 'is_active']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    list_editable = ['is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'publish_date', 'is_active')
        }),
        ('Содержание', {
            'fields': ('content', 'image'),
            'classes': ('wide',)
        }),
    )
    
    def short_content(self, obj):
        return Truncator(obj.content).chars(100)
    short_content.short_description = 'Краткое содержание'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'news_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def news_count(self, obj):
        return obj.news_set.count()
    news_count.short_description = 'Количество новостей'


@admin.register(NewsPageHero)
class NewsPageHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'preview_image', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'is_active', 'order')
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Рекомендуемый размер: 1920x600 пикселей'
        }),
        ('Кнопка', {
            'fields': ('show_button', 'button_text', 'button_link'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 150px; border-radius: 4px;" />', 
                obj.image.url
            )
        return "—"
    preview_image.short_description = 'Предпросмотр'


# ===== تسجيل نموذج المشتركين الجديد =====
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'consent', 'created_at', 'is_active']
    list_filter = ['consent', 'is_active', 'created_at']
    search_fields = ['email']
    list_editable = ['is_active']