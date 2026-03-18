# research/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import random
import string
from accounts.models import Company

class ResearchCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория исследований"
        verbose_name_plural = "Категории исследований"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Research(models.Model):
    RESEARCH_TYPES = [
        ('fundamental', 'Фундаментальные исследования'),
        ('business_management', 'Управление бизнесом и персоналом'),
        ('education', 'Исследования в образовании'),
        ('publishing', 'Издательско-полиграфические исследования'),
        ('psychological', 'Психологические исследования'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='research'
    )

    title = models.CharField(max_length=500, verbose_name="Название исследования")
    research_type = models.CharField(max_length=50, choices=RESEARCH_TYPES, verbose_name="Тип исследования")
    category = models.ForeignKey(ResearchCategory, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    image = models.ImageField(upload_to='research/', verbose_name="Изображение")
    publication_date = models.DateField(verbose_name="Дата публикации")
    author = models.CharField(max_length=200, verbose_name="Автор")
    file = models.FileField(upload_to='research/files/', blank=True, null=True, verbose_name="Файл исследования")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Исследование"
        verbose_name_plural = "Исследования"
        ordering = ['-publication_date', '-created_at']

    def __str__(self):
        return self.title


class ResearchTag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тега")
    research = models.ManyToManyField(Research, related_name='tags', verbose_name="Исследования")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Тег исследования"
        verbose_name_plural = "Теги исследований"

    def __str__(self):
        return self.name


class ResearchHero(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок (необязательно)", blank=True)
    background_image = models.ImageField(
        upload_to='research/hero/',
        verbose_name="Фоновое изображение",
        help_text="Рекомендуемый размер: широкий формат, например 1920x600"
    )
    brochure = models.FileField(
        upload_to='research/brochures/',
        blank=True, null=True,
        verbose_name='Брошюра конференций (PDF)',
        help_text='Загрузите PDF-файл с брошюрой конференций'
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero для исследований"
        verbose_name_plural = "Hero для исследований"

    def __str__(self):
        return self.title or f"Hero #{self.id}"


class Conference(models.Model):
    CONFERENCE_TYPES = [
        ('international', 'Международная'),
        ('national', 'Национальная'),
        ('regional', 'Региональная'),
        ('online', 'Онлайн'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='conferences'
    )

    title = models.CharField(max_length=500, verbose_name="Название конференции")
    conference_type = models.CharField(max_length=50, choices=CONFERENCE_TYPES, verbose_name="Тип конференции")
    description = models.TextField(verbose_name="Описание")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    image = models.ImageField(upload_to='conferences/', verbose_name="Изображение")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    location = models.CharField(max_length=300, verbose_name="Место проведения")
    registration_link = models.URLField(verbose_name="Ссылка для регистрации", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    contact_person = models.CharField(max_length=200, blank=True, verbose_name="Контактное лицо")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Контактный телефон")
    contact_email = models.EmailField(blank=True, verbose_name="Контактный email")
    organizers = models.TextField(blank=True, verbose_name="Организаторы")
    video = models.FileField(
        upload_to='conferences/videos/',
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
    file = models.FileField(
        upload_to='conferences/files/',
        blank=True, null=True,
        verbose_name="Файл конференции"
    )
    entrance_fee = models.CharField(
        max_length=100,
        default='бесплатно',
        verbose_name='Вход (плата)',
        help_text='Например: бесплатно, 500 руб, по приглашениям'
    )

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return self.title

    @property
    def can_register(self):
        return self.end_date >= timezone.now().date()


class ConferenceRegistration(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='conference_registrations'
    )

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='registrations', verbose_name="Конференция")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    agreement = models.BooleanField(verbose_name="Согласие с условиями")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Номер регистрации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Регистрация на конференцию"
        verbose_name_plural = "Регистрации на конференции"
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
        number = f"CONF-{date_part}-{random_part}"
        while ConferenceRegistration.objects.filter(registration_number=number).exists():
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            number = f"CONF-{date_part}-{random_part}"
        return number


class YouthCouncilDepartment(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название отделения")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отделение молодежного совета"
        verbose_name_plural = "Отделения молодежного совета"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class YouthCouncilMember(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    image = models.ImageField(upload_to='youth_council/', verbose_name="Фото")
    position = models.TextField(verbose_name="Должность")
    description = models.TextField(blank=True, verbose_name="Описание")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    departments = models.ManyToManyField(YouthCouncilDepartment, related_name='members', blank=True, verbose_name="Отделения")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Член молодежного ученого совета"
        verbose_name_plural = "Члены молодежного ученого совета"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name