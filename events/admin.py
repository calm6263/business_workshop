# events/admin.py
from django.contrib import admin
from django import forms
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import Event, InterestingProgram, EventRegistration, NewsletterSubscription, PageSettings, Album, Photo

# ===== Код для массовой загрузки нескольких изображений (используется только при добавлении) =====
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# Форма для добавления (поддерживает множественный выбор файлов)
class PhotoAdminAddForm(forms.ModelForm):
    image = MultipleFileField(label="Выберите одно или несколько изображений", required=False)

    class Meta:
        model = Photo
        fields = '__all__'

# Форма для редактирования (обычное поле для одного файла)
class PhotoAdminChangeForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput,
        }
# =====================================================================================

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'event', 'phone', 'email', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['full_name', 'phone', 'email', 'registration_number']
    readonly_fields = ['registration_number', 'created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('registration_number', 'event', 'full_name', 'phone', 'email', 'agreement')
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type_badge', 'date', 'price_display', 'is_active', 'order', 'preview_image', 'registrations_count', 'has_video']
    list_editable = ['is_active', 'order']
    list_filter = ['event_type', 'date', 'is_active']
    search_fields = ['title', 'short_description', 'detailed_description']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'event_type', 'short_description', 'detailed_description')
        }),
        ('Дата и время', {
            'fields': ('date', 'time')
        }),
        ('Стоимость и регистрация', {
            'fields': ('is_free', 'price', 'registration_url')
        }),
        ('Контактная информация', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('Место проведения и организаторы', {
            'fields': ('location', 'organizers')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Видео-инструкция', {
            'fields': ('video', 'video_title'),
            'description': 'Загрузите короткое видео (до 30 секунд) о том, как добраться до места проведения.'
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def event_type_badge(self, obj):
        colors = {
            'current': 'green',
            'upcoming': 'blue',
            'past': 'gray'
        }
        color = colors.get(obj.event_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, obj.get_event_type_display()
        )
    event_type_badge.short_description = 'Тип'
    
    def price_display(self, obj):
        return obj.price_display
    price_display.short_description = 'Стоимость'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Изображение'
    
    def registrations_count(self, obj):
        count = obj.registrations.count()
        return format_html(
            '<a href="{}?event__id__exact={}" style="background-color: #052946; color: white; padding: 2px 8px; border-radius: 12px; text-decoration: none;">{} регистраций</a>',
            f'/admin/events/eventregistration/', obj.id, count
        )
    registrations_count.short_description = 'Регистрации'
    
    def has_video(self, obj):
        return bool(obj.video)
    has_video.boolean = True
    has_video.short_description = 'Видео'

@admin.register(InterestingProgram)
class InterestingProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'cost_display', 'start_date', 'duration', 'is_active', 'order', 'preview_image']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'detailed_description', 'cost', 'start_date', 'duration')
        }),
        ('Изображения', {
            'fields': ('image', 'top_image'),
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Превью'

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at', 'subscribed_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'subscribed_at']

    fieldsets = (
        ('Информация о подписчике', {
            'fields': ('email', 'agreement', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'subscribed_at')
        }),
    )

@admin.register(PageSettings)
class PageSettingsAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'page_type', 'is_active', 'preview_hero_image', 'hero_title', 'updated_at']
    list_editable = ['is_active']
    list_filter = ['page_type', 'is_active']
    readonly_fields = ['updated_at']
    
    def preview_hero_image(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.hero_image.url)
        return "—"
    preview_hero_image.short_description = 'Главное изображение'
    
    fieldsets = (
        ('Информация о странице', {
            'fields': ('page_name', 'page_type', 'is_active')
        }),
        ('Главное изображение', {
            'fields': ('hero_image', 'hero_title', 'hero_subtitle')
        }),
        ('Сообщение об успешной подписке', {
            'fields': ('newsletter_success_image',),
            'description': 'Это изображение появится после успешной подписки на новости.'
        }),
        ('Временные метки', {
            'fields': ('updated_at',)
        }),
    )
    
    def has_add_permission(self, request):
        return True
    
    def changelist_view(self, request, extra_context=None):
        if not PageSettings.objects.filter(page_name='events_page').exists():
            self.message_user(request, "⚠️ Не найдены настройки страницы мероприятий. Будет использоваться настройки по умолчанию.", level='warning')
        if not PageSettings.objects.filter(page_name='gallery_page').exists():
            self.message_user(request, "⚠️ Не найдены настройки страницы фотогалереи. Будет использоваться настройки по умолчанию.", level='warning')
        return super().changelist_view(request, extra_context)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'photos_count', 'event_date', 'is_active', 'order', 'preview_cover']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'event_date')
        }),
        ('Изображения', {
            'fields': ('cover_image',)
        }),
        ('Настройки отображения', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def preview_cover(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.cover_image.url)
        return "—"
    preview_cover.short_description = 'Обложка'
    
    def photos_count(self, obj):
        count = obj.photos_count
        return format_html(
            '<a href="{}?album__id__exact={}" style="background-color: #7F1726; color: white; padding: 2px 8px; border-radius: 12px; text-decoration: none;">{} фото</a>',
            f'/admin/events/photo/', obj.id, count
        )
    photos_count.short_description = 'Фотографии'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['preview_image', 'album', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['album', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'album__title']
    
    list_per_page = 20
    list_max_show_all = 200
    show_full_result_count = False
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('album', 'title', 'description', 'order', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "—"
    preview_image.short_description = 'Превью'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return PhotoAdminAddForm
        else:
            return PhotoAdminChangeForm

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST' and request.FILES.getlist('image'):
            # استخدام النموذج للتحقق من البيانات بدلاً من request.POST مباشرة
            form = PhotoAdminAddForm(request.POST, request.FILES)
            if form.is_valid():
                album = form.cleaned_data['album']
                files = request.FILES.getlist('image')
                created_count = 0
                for f in files:
                    # إنشاء كائن Photo باستخدام البيانات المنظفة
                    photo = Photo(
                        album=album,
                        image=f,
                        title=form.cleaned_data.get('title', ''),
                        description=form.cleaned_data.get('description', ''),
                        order=form.cleaned_data.get('order', 0),
                        is_active=form.cleaned_data.get('is_active', True),
                    )
                    photo.save()
                    created_count += 1
                self.message_user(request, f"✅ Загружено {created_count} изображений.", level='SUCCESS')
                return redirect('admin:events_photo_changelist')
            else:
                # إذا كان النموذج غير صالح، نعرض الأخطاء
                for field, errors in form.errors.items():
                    for error in errors:
                        self.message_user(request, f"❌ {field}: {error}", level='ERROR')
                return super().add_view(request, form_url, extra_context)
        
        return super().add_view(request, form_url, extra_context)