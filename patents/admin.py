from django.contrib import admin
from .models import PatentImage

@admin.register(PatentImage)
class PatentImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at', 'short_caption')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'caption')
    fields = ('title', 'image', 'order', 'is_active', 'caption')

    def short_caption(self, obj):
        return obj.caption[:50] + '...' if obj.caption and len(obj.caption) > 50 else obj.caption
    short_caption.short_description = 'Краткий текст'