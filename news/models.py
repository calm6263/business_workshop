from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-publish_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class NewsPageHero(models.Model):
    title = models.CharField(
        max_length=200, 
        verbose_name="Заголовок",
        help_text="Заголовок для баннера на странице списка новостей"
    )
    subtitle = models.TextField(
        verbose_name="Подзаголовок",
        blank=True,
        help_text="Краткое описание под заголовком"
    )
    image = models.ImageField(
        upload_to='news/hero/', 
        verbose_name="Фоновое изображение",
        help_text="Рекомендуемый размер: 1920x600 пикселей"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Активно",
        help_text="Отображать баннер на странице"
    )
    show_button = models.BooleanField(
        default=True, 
        verbose_name="Показывать кнопку"
    )
    button_text = models.CharField(
        max_length=50, 
        default="Посмотреть все новости",
        verbose_name="Текст кнопки"
    )
    button_link = models.CharField(
        max_length=200, 
        default="#",
        verbose_name="Ссылка кнопки",
        help_text="Можно указать внутреннюю ссылку или внешнюю URL"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Порядок",
        help_text="Чем меньше число, тем выше отображается"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Баннер страницы новостей"
        verbose_name_plural = "Баннеры страницы новостей"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({'Активен' if self.is_active else 'Неактивен'})"


# ===== نموذج المشتركين الجديد =====
class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    consent = models.BooleanField(default=False, verbose_name="Согласие на обработку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return self.email