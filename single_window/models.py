# single_window/models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string
from accounts.models import Company

class BasicInfo(models.Model):
    address = models.TextField(verbose_name="Адрес", default="г. Москва, Садовая-Спасская 19к1\n(м. Красные ворота)")
    phone = models.CharField(verbose_name="Телефон", max_length=50, default="+7 (968) 418-44-88")
    email = models.EmailField(verbose_name="E-mail", default="info.fta@mail.ru")
    director = models.CharField(verbose_name="Руководитель", max_length=200, default="Солтанмурадова Заира Рустамовна")
    position_document = models.CharField(verbose_name="Название документа положения", max_length=300, default="Положение об услугах одного окна")
    position_file = models.FileField(verbose_name="Файл положения", upload_to='documents/', blank=True, null=True)
    department = models.CharField(verbose_name="Входит в состав", max_length=200, default="Управление развития персонала")
    working_days = models.CharField(verbose_name="Рабочие дни", max_length=100, default="Пн-Пт: 9:00 - 18:00")
    lunch_break = models.CharField(verbose_name="Обеденный перерыв", max_length=100, default="Обед: 13:00 - 14:00")
    weekend = models.CharField(verbose_name="Выходные", max_length=100, default="Сб-Вс: выходной")
    working_description = models.TextField(verbose_name="Описание графика работы", default="Мы готовы помочь вам в удобное время")

    class Meta:
        verbose_name = "Основные сведения"
        verbose_name_plural = "Основные сведения"

    def __str__(self):
        return "Основные сведения - услуги одного окна"


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок слайдера")
    subtitle = models.CharField(max_length=200, verbose_name="Подзаголовок", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='slider_images/', verbose_name="Изображение")
    link = models.URLField(verbose_name="Ссылка", blank=True)
    link_text = models.CharField(max_length=100, verbose_name="Текст ссылки", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдеры"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    SERVICE_CHOICES = [
        ('oformit-spravku', 'Оформить справку'),
        ('poluchit-dokumenty', 'Получить/Направить материнский капитал для обучения детей'),
        ('poluchit-materialnuyu-podderzhku', 'Получить материальную поддержку'),
        ('napravit-materinskiy-kapital', 'Направить материнский капитал для обучения детей'),
        ('oformit-chitatelskiy-bilet', 'Оформить читательский билет'),
        ('izmenit-lichnye-dannye', 'Изменить личные данные, отчислиться, оформить каникулы'),
        ('obrazovatelnyy-kredit', 'Образовательный кредит с господдержкой'),
        ('poluchit-lgotu', 'Получить льготу на образование'),
    ]
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="Услуга")
    question_number = models.IntegerField(verbose_name="Номер вопроса")
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['service', 'question_number']

    def __str__(self):
        return f"{self.get_service_display()} - Вопрос {self.question_number}"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершено'),
        ('rejected', 'Отклонено')
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='service_requests'
    )

    request_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")
    service_type = models.CharField(max_length=200, verbose_name="Тип услуги")
    format = models.CharField(max_length=200, verbose_name="Формат", blank=True)
    contact_person = models.CharField(max_length=200, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    additional_info = models.TextField(verbose_name="Дополнительные пожелания", blank=True)
    agreed_to_terms = models.BooleanField(verbose_name="Согласие с условиями")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=20, default='new', choices=STATUS_CHOICES, verbose_name="Статус")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    admin_notes = models.TextField(verbose_name="Примечания администратора", blank=True)

    class Meta:
        verbose_name = "Заявка на услугу"
        verbose_name_plural = "Заявки на услуги"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_number} - {self.service_type}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_request_number()
        super().save(*args, **kwargs)

    def generate_request_number(self):
        prefix = "REQ-"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}{random_part}"

    def get_status_display_class(self):
        status_classes = {
            'new': 'badge bg-primary',
            'in_progress': 'badge bg-warning',
            'completed': 'badge bg-success',
            'rejected': 'badge bg-danger'
        }
        return status_classes.get(self.status, 'badge bg-secondary')