from django.db import models
import random
import string
from django.utils import timezone

class HomePageSlider(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок", blank=True)
    subtitle = models.TextField(verbose_name="Подзаголовок", blank=True)
    image = models.ImageField(upload_to='home_sliders/', verbose_name="Изображение")
    button_text = models.CharField(max_length=100, verbose_name="Текст кнопки", default="Оставить заявку на партнерство")
    button_link = models.CharField(max_length=255, verbose_name="Ссылка кнопки", default="#")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Слайдер главной страницы"
        verbose_name_plural = "Слайдеры главной страницы"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else f"Слайдер {self.id}"


class Partner(models.Model):
    PARTNER_TYPES = [
        ('government', 'Государственные организации'),
        ('business', 'Бизнес-сообщество'),
        ('education', 'Образовательные учреждения'),
        ('other', 'Другие'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Название компании/организации")
    description = models.TextField(verbose_name="Описание")
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, verbose_name="Тип партнера")
    logo = models.ImageField(upload_to='partners/logos/', verbose_name="Логотип")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    show_in_carousel = models.BooleanField(default=True, verbose_name="Показывать в карусели")
    show_in_grid = models.BooleanField(default=True, verbose_name="Показывать в сетке")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class PartnershipApplication(models.Model):
    APPLICATION_TYPES = [
        ('physical', 'Физическое лицо'),
        ('legal', 'Юридическое лицо'),
    ]
    
    application_type = models.CharField(max_length=10, choices=APPLICATION_TYPES, verbose_name="Тип заявителя")
    company_name = models.CharField(max_length=255, verbose_name="Название компании")
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", blank=True)
    legal_address = models.TextField(verbose_name="Юридический адрес", blank=True)
    comments = models.TextField(verbose_name="Комментарии", blank=True)
    contact_person = models.CharField(max_length=200, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=[('pending', 'В ожидании'), ('processed', 'Обработано')], default='pending', verbose_name="Статус")
    request_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заявки", blank=True, null=True)
    
    class Meta:
        verbose_name = "Заявка на партнерство"
        verbose_name_plural = "Заявки на партнерство"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.get_application_type_display()}"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_request_number()
        super().save(*args, **kwargs)
    
    def generate_request_number(self):
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"REQ-{timestamp}-{random_chars}"


class LogoCarousel(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    
    class Meta:
        verbose_name = "Карусель логотипов"
        verbose_name_plural = "Карусели логотипов"
        ordering = ['order']
    
    def __str__(self):
        return self.partner.name