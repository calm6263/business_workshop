# models.py
from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", default="Правила посещения пространства")
    button_text = models.CharField(max_length=100, verbose_name="Текст кнопки", default="Стать башнером")
    description = models.TextField(
        verbose_name="Описание", 
        default="Мы создали пространство для тех, кто ценит тишину для концентрации, вдохновляющую атмосферу для творчества и гибкость для свободы выбора."
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдеры"
        ordering = ['order']
    
    def __str__(self):
        return self.title

class SliderImage(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE, verbose_name="Слайдер", related_name='images')
    image = models.ImageField(upload_to='slider/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Изображение слайдера"
        verbose_name_plural = "Изображения слайдера"
        ordering = ['order']
    
    def __str__(self):
        return self.caption if self.caption else f"Изображение слайдера {self.id}"

class Tariff(models.Model):
    TARIFF_TYPES = [
        ('trial', 'Пробный день'),
        ('flex', 'Гибкий график'),
        ('office', 'Закрытый кабинет'),
        ('meeting_room', 'Переговорный кабинет'),
        ('executive_office', 'Кабинет руководителя'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название тарифа")
    tariff_type = models.CharField(max_length=20, choices=TARIFF_TYPES, verbose_name="Тип тарифа")
    price = models.CharField(max_length=100, verbose_name="Цена", help_text="Например: Бесплатно, от 500 ₽ / час, от 2000 ₽ / день")
    image = models.ImageField(upload_to='tariffs/', blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание")
    button_text = models.CharField(max_length=100, default="Забронировать", verbose_name="Текст кнопки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ['order']
    
    def __str__(self):
        return self.title

class TariffFeature(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='tariff_features')
    feature_text = models.CharField(max_length=200, verbose_name="Особенность")
    icon_name = models.CharField(max_length=100, verbose_name="Название иконки", 
                               help_text="Например: material-symbols:work, solar:tea-cup-bold")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Особенность тарифа"
        verbose_name_plural = "Особенности тарифов"
        ordering = ['order']
    
    def __str__(self):
        return self.feature_text