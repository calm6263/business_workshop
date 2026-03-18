# models.py
from django.db import models
from django.core.validators import MaxLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
import uuid
from datetime import date

class ConsultationRequest(models.Model):
    DIRECTION_CHOICES = [
        ('hr_management', 'Управление персоналом организации'),
        ('psychology_management', 'Психология в менеджменте'),
        ('economic_theory', 'Экономическая теория'),
    ]

    request_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Уникальный номер заявки"
    )
    
    direction = models.CharField(
        max_length=100, 
        choices=DIRECTION_CHOICES, 
        verbose_name="Направление"
    )
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    contact_phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_email = models.EmailField(verbose_name="E-mail")
    additional_wishes = models.TextField(
        validators=[MaxLengthValidator(200)],
        blank=True,
        verbose_name="Дополнительные пожелания"
    )
    agreed_to_terms = models.BooleanField(default=False, verbose_name="Согласие с условиями")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{str(self.request_id)[:8].upper()} от {self.contact_email}"

    def get_short_request_id(self):
        return str(self.request_id)[:8].upper()
    
    def clean(self):
        errors = {}
        
        if self.date and self.date < date.today():
            errors['date'] = 'Дата консультации не может быть в прошлом'
            
        if self.contact_email:
            from django.core.validators import validate_email
            try:
                validate_email(self.contact_email)
            except ValidationError:
                errors['contact_email'] = 'Введите корректный email адрес'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class HeroSlide(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", blank=True)
    subtitle = models.CharField(max_length=300, verbose_name="Подзаголовок", blank=True)
    image = models.ImageField(
        upload_to='hero_slides/',
        verbose_name="Изображение",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'],
                message='Разрешены только файлы изображений (jpg, jpeg, png, webp, gif)'
            )
        ]
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Слайд героя"
        verbose_name_plural = "Слайды героя"
        ordering = ['order']
        
    def __str__(self):
        return f"Слайд {self.order}: {self.title}"
    
    def clean(self):
        errors = {}
        
        if self.title and len(self.title.strip()) < 3:
            errors['title'] = 'Заголовок должен содержать минимум 3 символа'
        
        if self.subtitle and len(self.subtitle.strip()) < 5:
            errors['subtitle'] = 'Подзаголовок должен содержать минимум 5 символов'
        
        # التحقق من أن الملف المرفوع هو صورة صالحة
        if self.image:
            try:
                img = Image.open(self.image)
                img.verify()  # يتحقق من سلامة الصورة دون تحميل كامل
            except Exception:
                errors['image'] = 'Файл повреждён или не является изображением.'
        
        if errors:
            raise ValidationError(errors)


class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ['order']
        
    def __str__(self):
        return self.question
    
    def clean(self):
        if len(self.question.strip()) < 5:
            raise ValidationError({'question': 'Вопрос должен содержать минимум 5 символов'})
        
        if len(self.answer.strip()) < 10:
            raise ValidationError({'answer': 'Ответ должен содержать минимум 10 символов'})


class SuccessPageImage(models.Model):
    image = models.ImageField(
        upload_to='success/',
        verbose_name="Изображение для страницы успеха",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Альтернативный текст")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение для успешной отправки"
        verbose_name_plural = "Изображения для успешной отправки"

    def __str__(self):
        return f"Изображение {self.id} - {self.alt_text[:30]}"

    def clean(self):
        errors = {}
        if self.image:
            try:
                img = Image.open(self.image)
                img.verify()
            except Exception:
                errors['image'] = 'Файл повреждён или не является изображением.'
        if errors:
            raise ValidationError(errors)