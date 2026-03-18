# events/models.py
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import random
import string
from accounts.models import Company

class Event(models.Model):
    EVENT_TYPES = [
        ('current', 'Идут сейчас'),
        ('upcoming', 'Предстоящие'),
        ('past', 'Прошедшие'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='events'
    )

    title = models.CharField(max_length=500, verbose_name="Название мероприятия")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='upcoming', verbose_name="Тип мероприятия")
    short_description = models.TextField(verbose_name="Краткое описание")
    detailed_description = models.TextField(blank=True, verbose_name="Подробное описание")
    image = models.ImageField(upload_to='events/', verbose_name="Изображение")
    date = models.DateField(verbose_name="Дата мероприятия")
    time = models.TimeField(blank=True, null=True, verbose_name="Время мероприятия")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость входа")
    is_free = models.BooleanField(default=False, verbose_name="Бесплатное мероприятие")
    registration_url = models.URLField(blank=True, verbose_name="Ссылка для регистрации")
    location = models.CharField(max_length=300, blank=True, verbose_name="Место проведения")
    contact_person = models.CharField(max_length=200, blank=True, verbose_name="Контактное лицо")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Контактный телефон")
    contact_email = models.EmailField(blank=True, verbose_name="Контактный email")
    organizers = models.TextField(blank=True, verbose_name="Организаторы")
    video = models.FileField(
        upload_to='events/videos/',
        blank=True, null=True,
        verbose_name="Видео (как дойти)",
        help_text="Загрузите короткое видео (до 30 секунд, MP4) о том, как добраться до места."
    )
    video_title = models.CharField(
        max_length=200,
        blank=True,
        default="Как дойти?",
        verbose_name="Заголовок видео"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['event_type', 'date', 'order']

    def __str__(self):
        return f"{self.date} - {self.title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', kwargs={'pk': self.pk})

    @property
    def price_display(self):
        if self.is_free:
            return "бесплатно"
        return f"{self.price:,.0f} ₽".replace(',', ' ')

    @property
    def can_register(self):
        if self.event_type == 'past':
            return False
        return self.date >= timezone.now().date()


class EventRegistration(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='event_registrations'
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name="Мероприятие")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    agreement = models.BooleanField(verbose_name="Согласие с условиями")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Номер регистрации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Регистрация на мероприятие"
        verbose_name_plural = "Регистрации на мероприятия"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.registration_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = self.generate_registration_number()
        super().save(*args, **kwargs)

    def generate_registration_number(self):
        date_part = timezone.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        number = f"REG-{date_part}-{random_part}"
        while EventRegistration.objects.filter(registration_number=number).exists():
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            number = f"REG-{date_part}-{random_part}"
        return number


class InterestingProgram(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='interesting_programs'
    )

    title = models.CharField(max_length=200, verbose_name="Название программы")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(upload_to='interesting_programs/', verbose_name="Изображение")
    top_image = models.ImageField(upload_to='interesting_programs/top/', verbose_name="Верхнее изображение", blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    start_date = models.CharField(max_length=100, verbose_name="Начало обучения")
    duration = models.CharField(max_length=100, verbose_name="Длительность")
    description = models.TextField(blank=True, verbose_name="Описание")
    detailed_description = models.TextField(blank=True, verbose_name="Подробное описание")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Интересная программа"
        verbose_name_plural = "Интересные программы"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while InterestingProgram.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def cost_display(self):
        return f"{self.cost:,.0f} ₽".replace(',', ' ')


class NewsletterSubscription(models.Model):
    # هذه النشرة البريدية قد تكون عامة (لجميع الشركات) أو لكل شركة على حدة. نتركها عامة.
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    agreement = models.BooleanField(verbose_name="Согласие с условиями", default=False)
    is_active = models.BooleanField(verbose_name="Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    subscribed_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Подписка на рассылку"
        verbose_name_plural = "Подписки на рассылку"
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class PageSettings(models.Model):
    # إعدادات الصفحة عامة
    PAGE_CHOICES = [
        ('events_page', 'Страница мероприятий'),
        ('gallery_page', 'Страница фотогалереи'),
    ]
    page_name = models.CharField(max_length=100, verbose_name="Название страницы", unique=True, default='events_page')
    page_type = models.CharField(max_length=20, choices=PAGE_CHOICES, default='events_page', verbose_name="Тип страницы")
    hero_image = models.ImageField(
        upload_to='page_hero/',
        verbose_name="Главное изображение",
        blank=True, null=True,
        default='page_hero/default_hero.jpg'
    )
    hero_title = models.CharField(max_length=200, verbose_name="Заголовок изображения", default='Мероприятия')
    hero_subtitle = models.TextField(verbose_name="Подзаголовок изображения", blank=True, default='Присоединяйтесь к нашим событиям')
    is_active = models.BooleanField(default=True, verbose_name="Активировать изображение")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    newsletter_success_image = models.ImageField(
        upload_to='newsletter/',
        blank=True, null=True,
        verbose_name="Изображение успешной подписки",
        help_text="Это изображение появится после успешной подписки на новости."
    )

    class Meta:
        verbose_name = "Настройки страницы"
        verbose_name_plural = "Настройки страниц"
        ordering = ['page_name']

    def __str__(self):
        return f"Настройки {self.page_name}"

    def get_hero_image_url(self):
        if self.hero_image and hasattr(self.hero_image, 'url'):
            return self.hero_image.url
        return '/static/events/images/default_hero.jpg'

    def save(self, *args, **kwargs):
        if not self.pk and PageSettings.objects.filter(page_name=self.page_name).exists():
            existing = PageSettings.objects.get(page_name=self.page_name)
            existing.hero_image = self.hero_image if self.hero_image else existing.hero_image
            existing.hero_title = self.hero_title
            existing.hero_subtitle = self.hero_subtitle
            existing.is_active = self.is_active
            existing.newsletter_success_image = self.newsletter_success_image
            return existing.save(*args, **kwargs)
        return super().save(*args, **kwargs)


class Album(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='albums'
    )

    title = models.CharField(max_length=200, verbose_name="Название альбома")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка")
    description = models.TextField(blank=True, verbose_name="Описание альбома")
    cover_image = models.ImageField(upload_to='albums/covers/', verbose_name="Обложка альбома")
    event_date = models.DateField(verbose_name="Дата события", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['-event_date', 'order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Album.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('album_detail', kwargs={'slug': self.slug})

    @property
    def photos_count(self):
        return self.photos.filter(is_active=True).count()


class Photo(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='photos'
    )

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name="Альбом")
    title = models.CharField(max_length=200, verbose_name="Название фотографии", blank=True)
    image = models.ImageField(upload_to='albums/photos/', verbose_name="Фотография")
    description = models.TextField(blank=True, verbose_name="Описание фотографии")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ['album', 'order', 'created_at']

    def __str__(self):
        return self.title if self.title else f"Фотография {self.id}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Фотография {self.album.title} {self.order}"
        super().save(*args, **kwargs)