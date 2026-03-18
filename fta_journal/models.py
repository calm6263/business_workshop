from django.db import models
from django.urls import reverse
from django.utils import timezone

class JournalIssue(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название выпуска")
    description = models.TextField(verbose_name="Описание")
    cover_image = models.ImageField(upload_to='journal/covers/', verbose_name="Изображение обложки")
    publication_date = models.DateField(default=timezone.now, verbose_name="Дата публикации")
    pdf_file = models.FileField(upload_to='journal/pdfs/', blank=True, null=True, verbose_name="PDF файл")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    show_in_best = models.BooleanField(default=False, verbose_name="Показать в разделе Лучшее")
    show_in_new = models.BooleanField(default=False, verbose_name="Показать в разделе Новые поступления")
    best_order = models.IntegerField(default=0, verbose_name="Порядок в разделе Лучшее")
    new_order = models.IntegerField(default=0, verbose_name="Порядок в разделе Новые поступления")
    
    class Meta:
        verbose_name = "Выпуск журнала"
        verbose_name_plural = "Выпуски журнала"
        ordering = ['-publication_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('fta_journal:journal_home')


class SliderImage(models.Model):
    CAROUSEL_CHOICES = [
        ('main', 'Main Slider'),
        ('best', 'Лучшее Carousel'),
        ('early', 'Ранние выпуски Carousel'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название изображения")
    image = models.ImageField(upload_to='slider/', verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание изображения")
    link = models.URLField(blank=True, verbose_name="Ссылка на изображение")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    carousel_type = models.CharField(
        max_length=10, 
        choices=CAROUSEL_CHOICES, 
        default='main', 
        verbose_name="Тип карусели"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Изображение слайдера"
        verbose_name_plural = "Изображения слайдера"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class SectionSettings(models.Model):
    best_section_title = models.CharField(
        max_length=100, 
        default="Лучшее", 
        verbose_name="Название раздела Лучшее"
    )
    new_section_title = models.CharField(
        max_length=100, 
        default="Новые поступления", 
        verbose_name="Название раздела Новые поступления"
    )
    early_section_title = models.CharField(
        max_length=100, 
        default="Ранние выпуски", 
        verbose_name="Название раздела Ранние выпуски"
    )
    
    class Meta:
        verbose_name = "Настройки разделов"
        verbose_name_plural = "Настройки разделов"
    
    def __str__(self):
        return "Настройки разделов"
    
    def save(self, *args, **kwargs):
        if not self.pk and SectionSettings.objects.exists():
            existing = SectionSettings.objects.first()
            existing.best_section_title = self.best_section_title
            existing.new_section_title = self.new_section_title
            existing.early_section_title = self.early_section_title
            return existing.save(*args, **kwargs)
        return super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class IssuePage(models.Model):
    issue = models.ForeignKey(
        JournalIssue,
        on_delete=models.CASCADE,
        related_name='pages',
        verbose_name="Выпуск"
    )
    image = models.ImageField(upload_to='journal/pages/', verbose_name="Изображение страницы")
    page_number = models.PositiveIntegerField(verbose_name="Номер страницы")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Страница выпуска"
        verbose_name_plural = "Страницы выпусков"
        ordering = ['issue', 'order', 'page_number']

    def __str__(self):
        return f"{self.issue.title} - стр. {self.page_number}"