from django.db import models
from django.core.exceptions import ValidationError
import random
import string

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    slug = models.SlugField(unique=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
    
    def __str__(self):
        return self.title

class Slide(models.Model):
    SLIDE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Title")
    slide_type = models.CharField(max_length=10, choices=SLIDE_TYPES, default='image', verbose_name="Slide Type")
    image = models.ImageField(upload_to='slides/', blank=True, null=True, verbose_name="Image")
    video = models.FileField(upload_to='slides/videos/', blank=True, null=True, verbose_name="Video File")
    caption = models.TextField(blank=True, verbose_name="Caption")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Order")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ['order', 'created_at']
    
    def clean(self):
        if self.slide_type == 'image' and not self.image:
            raise ValidationError({'image': 'Image is required for image slides'})
        if self.slide_type == 'video' and not self.video:
            raise ValidationError({'video': 'Video is required for video slides'})
    
    def __str__(self):
        return self.title

class Application(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'В обработке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('completed', 'Завершена'),
    ]
    
    application_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")
    contact_person = models.CharField(max_length=200, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    additional_notes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = self.generate_application_number()
        super().save(*args, **kwargs)
    
    def generate_application_number(self):
        prefix = "LN"
        random_digits = ''.join(random.choices(string.digits, k=6))
        application_number = f"{prefix}{random_digits}"
        
        while Application.objects.filter(application_number=application_number).exists():
            random_digits = ''.join(random.choices(string.digits, k=6))
            application_number = f"{prefix}{random_digits}"
        
        return application_number
    
    def __str__(self):
        return f"{self.application_number} - {self.contact_person}"

class Document(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название документа")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class EducationalProgram(models.Model):
    PROGRAM_TYPES = [
        ('professional_retraining', 'Профессиональная переподготовка'),
        ('qualification_upgrade', 'Повышение квалификации'),
        ('coaching', 'Коучинг'),
        ('training', 'Тренинг'),
        ('online', 'Онлайн'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название программы")
    program_type = models.CharField(max_length=50, choices=PROGRAM_TYPES, verbose_name="Тип программы")
    description = models.TextField(verbose_name="Описание программы")
    image = models.ImageField(upload_to='programs/', verbose_name="Изображение")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость", blank=True, null=True)
    start_date = models.DateField(verbose_name="Дата начала", blank=True, null=True)
    duration = models.CharField(max_length=100, verbose_name="Длительность", blank=True, null=True)
    program_count = models.IntegerField(default=0, verbose_name="Количество программ")
    is_featured = models.BooleanField(default=False, verbose_name="Показывать в интересных программах")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class License(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to='licenses/', verbose_name="Файл")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title