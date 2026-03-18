# applicants/models.py
from django.db import models
import random
import string
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
from accounts.models import Company  # استيراد Company

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10 MB
        raise ValidationError("Максимальный размер файла 10 МБ")

class ApplicantsPage(models.Model):
    # ... (نفس الكود السابق)
    title = models.CharField(max_length=200, default='Поступающим', verbose_name="Заголовок")
    background_image = models.ImageField(upload_to='applicants/', blank=True, null=True, verbose_name="Фоновое изображение")
    rocket_image = models.ImageField(upload_to='applicants/', blank=True, null=True, verbose_name="Изображение ракеты")
    conditions_file = models.FileField(
        upload_to='applicants/conditions/',
        blank=True, null=True,
        verbose_name="Файл с условиями приема",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    enrollment_conditions_file = models.FileField(
        upload_to='applicants/enrollment_conditions/',
        blank=True, null=True,
        verbose_name="Файл с условиями поступления",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    programs_list_file = models.FileField(
        upload_to='applicants/programs_list/',
        blank=True, null=True,
        verbose_name="Файл с перечнем образовательных программ",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    benefits_file = models.FileField(
        upload_to='applicants/benefits/',
        blank=True, null=True,
        verbose_name="Файл с льготами и особыми условиями",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    contract_sample_file = models.FileField(
        upload_to='applicants/contracts/',
        blank=True, null=True,
        verbose_name="Образец договора на обучение",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    useful_links_file = models.FileField(
        upload_to='applicants/useful_links/',
        blank=True, null=True,
        verbose_name="Полезные ссылки и документы",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), validate_file_size]
    )
    methods_review_text = models.CharField(
        max_length=300,
        blank=True,
        default="Заявки рассматриваются в течение пяти рабочих дней с момента подачи.",
        verbose_name="Текст о рассмотрении заявок"
    )
    methods_login_text = models.CharField(
        max_length=300,
        blank=True,
        default="Для подачи документов дистанционно нужно авторизироваться в личном кабинете.",
        verbose_name="Текст об авторизации"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Страница Поступающим"
        verbose_name_plural = "Страница Поступающим"

    def __str__(self):
        return self.title


class ApplicationMethod(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    icon_svg = models.TextField(verbose_name="SVG иконки", help_text="Вставьте код SVG основной иконки")
    question_svg = models.TextField(verbose_name="SVG знака вопроса", help_text="Вставьте код SVG знака вопроса (можно одинаковый для всех)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Способ подачи документов"
        verbose_name_plural = "Способы подачи документов"
        ordering = ['order']

    def __str__(self):
        return self.title


class EnrollmentStage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название этапа")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        upload_to='enrollment_stages/',
        verbose_name="Изображение этапа",
        help_text="Загрузите изображение (PNG, JPG, JPEG)",
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg'])]
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Этап зачисления"
        verbose_name_plural = "Этапы зачисления"
        ordering = ['order']

    def __str__(self):
        return self.name


class ApplicantDocument(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название документа")
    file = models.FileField(
        upload_to='applicant_documents/',
        verbose_name="Файл",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png']), validate_file_size]
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Документ для поступающих"
        verbose_name_plural = "Документы для поступающих"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ApplicantApplication(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'В обработке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('completed', 'Завершена'),
    ]

    # ربط مع الشركة
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='applicant_applications'
    )

    application_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")
    contact_person = models.CharField(
        max_length=200,
        verbose_name="Контактное лицо",
        validators=[RegexValidator(regex=r'^[^<>{}()\[\]\\\/$%^&*+=|~`]+$', message='Имя содержит недопустимые символы.')]
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    additional_notes = models.TextField(blank=True, default='', verbose_name="Дополнительные пожелания")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка поступающего"
        verbose_name_plural = "Заявки поступающих"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = self.generate_application_number()
        super().save(*args, **kwargs)

    def generate_application_number(self):
        prefix = "AP"
        random_digits = ''.join(random.choices(string.digits, k=6))
        application_number = f"{prefix}{random_digits}"
        while ApplicantApplication.objects.filter(application_number=application_number).exists():
            random_digits = ''.join(random.choices(string.digits, k=6))
            application_number = f"{prefix}{random_digits}"
        return application_number

    def __str__(self):
        return f"{self.application_number} - {self.contact_person}"

    def clean(self):
        if len(self.phone) < 10:
            raise ValidationError({'phone': 'Номер телефона слишком короткий'})