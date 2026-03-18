from django.db import models
from django.urls import reverse

class HeroImage(models.Model):
    """Модель для изображений героев на страницах"""
    PAGE_CHOICES = [
        ('departments_list', 'Страница списка отделений'),
        ('department_detail', 'Страница деталей отделения'),
    ]
    
    page = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        unique=True,
        verbose_name="Страница"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        blank=True
    )
    subtitle = models.CharField(
        max_length=300,
        verbose_name="Подзаголовок",
        blank=True
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    image = models.ImageField(
        upload_to='hero_images/',
        verbose_name="Изображение героя"
    )
    link_text = models.CharField(
        max_length=100,
        verbose_name="Текст ссылки",
        blank=True
    )
    link = models.CharField(
        max_length=200,
        verbose_name="Ссылка",
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = "Изображение героя"
        verbose_name_plural = "Изображения героев"
        ordering = ['order', 'page']
    
    def __str__(self):
        return f"{self.get_page_display()} - {self.title or 'Без заголовка'}"


class Department(models.Model):
    PROGRAM_TYPES = [
        ('economics', 'Отделение экономики и управления'),
        ('psychology', 'Отделение психологии'), 
        ('law', 'Отделение юриспруденции'),
        ('design', 'Отделение дизайна'),
        ('management', 'Отделение менеджмента'),
        ('development', 'Иные форматы развития'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название отделения")
    program_type = models.CharField(max_length=50, choices=PROGRAM_TYPES, verbose_name="Тип программы")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='departments/', verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Отделение"
        verbose_name_plural = "Отделения"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('departments:department_detail', kwargs={'pk': self.pk})
    
    @property
    def programs_count(self):
        """Количество программ, связанных с этим отделением"""
        return self.programs.count()