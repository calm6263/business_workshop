from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import (
    ValuesSection, StatisticsSection, PhotoAlbum, GalleryImage,
    LeaderSpeech, LeaderSpeechVideo, MainSlider, DownloadableFile,
    Leadership, QuoteSection, AcademyTeamMember   # استيراد النموذج الجديد
)


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 20
    fields = ['image', 'preview_image', 'order', 'is_active']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "Нет фото"
    preview_image.short_description = "Предпросмотр"


class ValuesSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'show_dot', 'show_arrow', 'created_at']
    list_editable = ['order', 'is_active', 'show_dot', 'show_arrow']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'quote_1', 'quote_2', 'content']
    readonly_fields = ['created_at', 'updated_at', 'preview_rocket_image']
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'is_active']
        }),
        ('Контент раздела', {
            'fields': ['rocket_image', 'preview_rocket_image', 'quote_1', 'quote_2', 'content']
        }),
        ('Настройки отображения', {
            'fields': ['order', 'show_dot', 'show_arrow']
        }),
        ('Даты', {
            'fields': [('created_at', 'updated_at')],
            'classes': ['collapse']
        }),
    ]

    def preview_rocket_image(self, obj):
        if obj.rocket_image:
            return format_html('<img src="{}" width="200" style="max-height: 200px; object-fit: contain;" />', 
                             obj.rocket_image.url)
        return "Изображение ракеты не загружено"
    preview_rocket_image.short_description = "Предпросмотр ракеты"


class StatisticsSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'show_dot', 'show_arrow', 'created_at']
    list_editable = ['order', 'is_active', 'show_dot', 'show_arrow']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'stat_title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'is_active']
        }),
        ('Заголовок статистики', {
            'fields': ['stat_title']
        }),
        ('Статистика 1', {
            'fields': ['stat_number_1', 'stat_label_1']
        }),
        ('Статистика 2', {
            'fields': ['stat_number_2', 'stat_label_2']
        }),
        ('Статистика 3', {
            'fields': ['stat_number_3', 'stat_label_3']
        }),
        ('Дополнительный контент', {
            'fields': ['content'],
            'classes': ['collapse']
        }),
        ('Настройки отображения', {
            'fields': ['order', 'show_dot', 'show_arrow']
        }),
        ('Даты', {
            'fields': [('created_at', 'updated_at')],
            'classes': ['collapse']
        }),
    ]


class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'preview_cover']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['preview_cover']
    inlines = [GalleryImageInline]
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'is_active']
        }),
        ('Обложка альбома', {
            'fields': ['cover_image', 'preview_cover']
        }),
        ('Описание альбома', {
            'fields': ['description']
        }),
        ('Настройки отображения', {
            'fields': ['order']
        }),
    ]

    def preview_cover(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="200" style="max-height: 200px; object-fit: contain;" />', 
                             obj.cover_image.url)
        return "Обложка не загружена"
    preview_cover.short_description = "Предпросмотр обложки"


# نموذج مخصص لدعم التحميل المتعدد للصور
class GalleryImageAdminForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة خاصية multiple إلى واجهة اختيار الملف
        self.fields['image'].widget.attrs.update({'multiple': True})
        self.fields['image'].help_text = "Можно выбрать несколько файлов одновременно (используйте Ctrl или Shift)"


from PIL import Image
...

class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageAdminForm
    list_display = ['thumbnail_preview', 'album', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'album']
    search_fields = ['id']
    readonly_fields = ['thumbnail_preview']
    
    fieldsets = [
        ('Фото', {
            'fields': ['album', 'image', 'thumbnail_preview']
        }),
        ('Настройки отображения', {
            'fields': ['order', 'is_active']
        }),
    ]

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "Нет фото"
    thumbnail_preview.short_description = "Предпросмотр"

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            files = request.FILES.getlist('image')
            album = form.cleaned_data.get('album')
            order = form.cleaned_data.get('order', 0)
            is_active = form.cleaned_data.get('is_active', True)

            saved_count = 0
            errors = []
            for f in files:
                try:
                    # التحقق من أن الملف صورة صالحة باستخدام Pillow
                    img = Image.open(f)
                    img.verify()  # التحقق من سلامة الصورة
                    f.seek(0)  # إعادة المؤشر بعد التحقق
                    GalleryImage.objects.create(
                        album=album,
                        image=f,
                        order=order,
                        is_active=is_active
                    )
                    saved_count += 1
                except Exception as e:
                    errors.append(f"{f.name}: {str(e)}")

            if errors:
                self.message_user(
                    request,
                    f"Сохранено {saved_count} фото. Ошибки: {', '.join(errors)}",
                    level='ERROR'
                )
            else:
                self.message_user(request, f"Сохранено {saved_count} фото.")

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('admin:about_academy_galleryimage_changelist'))


class LeaderSpeechVideoInline(admin.TabularInline):
    model = LeaderSpeechVideo
    extra = 1
    fields = ['title', 'video_url', 'video_file', 'thumbnail', 'order', 'is_active', 'preview_thumbnail']
    readonly_fields = ['preview_thumbnail']

    def preview_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', 
                             obj.thumbnail.url)
        return "Нет превью"
    preview_thumbnail.short_description = "Превью"


class LeaderSpeechAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    fields = ['title', 'is_active', 'order']
    inlines = [LeaderSpeechVideoInline]


class MainSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'preview_image']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['preview_image']
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'description', 'is_active']
        }),
        ('Изображение слайда', {
            'fields': ['image', 'preview_image']
        }),
        ('Настройки отображения', {
            'fields': ['order']
        }),
    ]

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="max-height: 150px; object-fit: contain;" />', 
                             obj.image.url)
        return "Изображение не загружено"
    preview_image.short_description = "Предпросмотр"


class DownloadableFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type', 'button_text', 'order', 'is_active', 'position_right', 'preview_button']
    list_editable = ['order', 'is_active', 'position_right']
    list_filter = ['is_active', 'file_type', 'position_right']
    search_fields = ['title', 'button_text', 'description']
    readonly_fields = ['created_at', 'updated_at', 'preview_button']
    
    fieldsets = [
        ('Информация о файле', {
            'fields': ['title', 'description', 'file_type', 'file'],
            'description': 'Поддерживаемые форматы: PDF, Excel (.xlsx, .xls), Word (.docx, .doc), PowerPoint (.pptx, .ppt)'
        }),
        ('Настройки кнопки', {
            'fields': ['button_text', 'button_color', 'text_color', 'show_icon']
        }),
        ('Настройки отображения', {
            'fields': ['order', 'is_active', 'position_right']
        }),
        ('Предпросмотр кнопки', {
            'fields': ['preview_button'],
            'classes': ['collapse']
        }),
        ('Даты', {
            'fields': [('created_at', 'updated_at')],
            'classes': ['collapse']
        }),
    ]
    
    def preview_button(self, obj):
        if obj.is_active:
            color_style = f"background-color: {obj.button_color}; color: {obj.text_color};"
            return format_html(
                '''
                <div style="{} padding: 15px; border-radius: 10px; margin: 10px 0; max-width: 400px;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="background: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                <i class="fas {}" style="font-size: 20px;"></i>
                            </div>
                            <div>
                                <div style="font-weight: bold; font-size: 16px;">{}</div>
                                <div style="font-size: 12px; opacity: 0.9;">{}</div>
                            </div>
                        </div>
                        <div style="font-size: 20px;">⬇️</div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #666;">
                        Расположение: {} | Статус: {}
                    </div>
                </div>
                ''',
                color_style,
                obj.get_file_icon(),
                obj.button_text,
                obj.title,
                "Справа" if obj.position_right else "Слева",
                "Активен" if obj.is_active else "Не активен"
            )
        return "Не активен"
    
    preview_button.short_description = "Предпросмотр кнопки"


class LeadershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    fields = ['name', 'position', 'image', 'description', 'email', 'phone', 'order', 'is_active']
    search_fields = ['name', 'position']

    def short_position(self, obj):
        return obj.position[:50] + "…" if len(obj.position) > 50 else obj.position
    short_position.short_description = "Должность"


class QuoteSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    fields = ['title', 'quote_text', 'image', 'is_active', 'order']


# ===== تسجيل النموذج الجديد =====
@admin.register(AcademyTeamMember)
class AcademyTeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'rank_colored', 'department', 'order', 'is_active', 'preview_image']
    list_editable = ['order', 'is_active']
    list_filter = ['rank', 'department', 'is_active']
    search_fields = ['name', 'position', 'email', 'phone']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'image', 'position', 'description')
        }),
        ('Контакты', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Категория и порядок', {
            'fields': ('department', 'rank', 'order', 'is_active')
        }),
    )

    def rank_colored(self, obj):
        colors = {
            'director': '#7F1726',
            'deputy_director': '#052946',
            'teacher': '#2E7D32',
            'employee': '#FF8F00',
        }
        color = colors.get(obj.rank, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px;">{}</span>',
            color, obj.get_rank_display()
        )
    rank_colored.short_description = "Ранг"

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.image.url)
        return "—"
    preview_image.short_description = "Фото"


# تسجيل النماذج الموجودة
admin.site.register(ValuesSection, ValuesSectionAdmin)
admin.site.register(StatisticsSection, StatisticsSectionAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(LeaderSpeech, LeaderSpeechAdmin)
admin.site.register(MainSlider, MainSliderAdmin)
admin.site.register(DownloadableFile, DownloadableFileAdmin)
admin.site.register(Leadership, LeadershipAdmin)
admin.site.register(QuoteSection, QuoteSectionAdmin)