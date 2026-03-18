# press_center/models.py
from django.db import models
import random
import string
from accounts.models import Company

class PressCenterPage(models.Model):
    title = models.CharField(max_length=200, default='Пресс-центр', verbose_name="Заголовок")
    background_image = models.ImageField(upload_to='press_center/', verbose_name="Фоновое изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    publication_rules_file = models.FileField(
        upload_to='press_center/rules/',
        verbose_name="Файл правил публикации",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Страница Пресс-центра"
        verbose_name_plural = "Страница Пресс-центра"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            PressCenterPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class PressCenterImage(models.Model):
    press_center = models.ForeignKey(PressCenterPage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='press_center/images/', verbose_name="Изображение")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")

    class Meta:
        verbose_name = "Изображение Пресс-центра"
        verbose_name_plural = "Изображения Пресс-центра"
        ordering = ['order']

    def __str__(self):
        return f"Изображение {self.id} для {self.press_center.title}"


class PublicationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('rejected', 'Отклонено'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='publication_requests'
    )

    request_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки", blank=True)
    organization = models.CharField(max_length=200, verbose_name="Название организации")
    theme = models.CharField(max_length=200, verbose_name="Тема публикации")
    desired_dates = models.CharField(max_length=100, verbose_name="Желаемые даты публикации")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")
    additional_wishes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка на публикацию"
        verbose_name_plural = "Заявки на публикацию"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.organization} - {self.theme}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_request_number()
        super().save(*args, **kwargs)

    def generate_request_number(self):
        prefix = "PR"
        random_digits = ''.join(random.choices(string.digits, k=6))
        request_number = f"{prefix}{random_digits}"
        while PublicationRequest.objects.filter(request_number=request_number).exists():
            random_digits = ''.join(random.choices(string.digits, k=6))
            request_number = f"{prefix}{random_digits}"
        return request_number