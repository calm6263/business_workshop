# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Slider, SliderImage, Tariff, TariffFeature

class SliderImageInline(admin.TabularInline):
    model = SliderImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    inlines = [SliderImageInline]

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['slider', 'caption', 'order', 'preview_image']
    list_editable = ['order']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Превью'

class TariffFeatureInline(admin.TabularInline):
    model = TariffFeature
    extra = 1
    fields = ['feature_text', 'icon_name', 'order']

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['title', 'tariff_type', 'price', 'is_active', 'order', 'preview_image']
    list_editable = ['is_active', 'order']
    list_filter = ['tariff_type', 'is_active']
    inlines = [TariffFeatureInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'tariff_type', 'price', 'image', 'description', 'button_text')
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Превью'

@admin.register(TariffFeature)
class TariffFeatureAdmin(admin.ModelAdmin):
    list_display = ['tariff', 'feature_text', 'icon_name', 'order']
    list_editable = ['order']
    list_filter = ['tariff']