# patents/models.py
from django.db import models
from accounts.models import Company

class PatentImage(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='patent_images'
    )

    title = models.CharField('Название (необязательно)', max_length=200, blank=True, help_text='Название изображения, отображаемое при наведении')
    image = models.ImageField('Изображение', upload_to='patents/')
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Порядок отображения в слайдере')
    is_active = models.BooleanField('Активно', default=True, help_text='Показывать изображение в слайдере')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    caption = models.TextField('Текст под изображением', blank=True, help_text='Отображается под слайдером, можно использовать длинный текст')

    class Meta:
        verbose_name = 'Изображение патента'
        verbose_name_plural = 'Изображения патентов'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title or f"Изображение {self.id}"