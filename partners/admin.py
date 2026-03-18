from django.contrib import admin
from .models import Partner, PartnershipApplication, HomePageSlider, LogoCarousel

@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'button_text', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'show_in_carousel', 'show_in_grid', 'order', 'is_active', 'created_at']
    list_editable = ['show_in_carousel', 'show_in_grid', 'order', 'is_active']
    list_filter = ['partner_type', 'is_active', 'show_in_carousel', 'show_in_grid']
    search_fields = ['name', 'description']


@admin.register(PartnershipApplication)
class PartnershipApplicationAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'company_name', 'application_type', 'contact_person', 'phone', 'status', 'created_at']
    list_filter = ['application_type', 'status', 'created_at']
    search_fields = ['company_name', 'contact_person', 'phone', 'request_number']
    readonly_fields = ['created_at', 'request_number']
    fieldsets = (
        ('Основная информация', {
            'fields': ('request_number', 'application_type', 'company_name', 'contact_person', 'phone', 'email', 'status')
        }),
        ('Детали для юридических лиц', {
            'fields': ('inn', 'kpp', 'legal_address'),
            'classes': ('collapse',)
        }),
        ('Дополнительная информация', {
            'fields': ('comments', 'created_at')
        }),
    )


@admin.register(LogoCarousel)
class LogoCarouselAdmin(admin.ModelAdmin):
    list_display = ['partner', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['partner__name']