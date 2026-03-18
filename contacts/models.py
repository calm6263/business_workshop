from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactSection(models.Model):
    SECTION_TYPES = [
        ('documents', 'Прием документов'),
        ('services', 'Услуги одного окна'),
        ('media', 'Контакты для СМИ'),
        ('it', 'Техническая поддержка IT'),
        ('general', 'Общие контакты'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название раздела")
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True, verbose_name="Тип раздела")
    department_name = models.CharField(max_length=200, blank=True, verbose_name="Название отдела/подразделения")
    description = models.TextField(blank=True, verbose_name="Описание раздела")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    additional_phones = models.JSONField(default=list, blank=True, verbose_name="Дополнительные телефоны")
    additional_emails = models.JSONField(default=list, blank=True, verbose_name="Дополнительные email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    work_hours = models.TextField(blank=True, verbose_name="Время работы")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Раздел контактов"
        verbose_name_plural = "Разделы контактов"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class OrganizationInfo(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название организации")
    full_name = models.CharField(max_length=500, verbose_name="Полное наименование")
    general_phone = models.CharField(max_length=20, verbose_name="Основной телефон")
    general_email = models.EmailField(verbose_name="Основной email")
    additional_phones = models.JSONField(default=list, blank=True, verbose_name="Дополнительные телефоны")
    address = models.TextField(verbose_name="Юридический адрес")
    description = models.TextField(blank=True, verbose_name="Описание организации")
    logo = models.ImageField(upload_to='contacts/logos/', blank=True, null=True, verbose_name="Логотип")
    
    class Meta:
        verbose_name = "Информация об организации"
        verbose_name_plural = "Информация об организации"
    
    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название соцсети")
    url = models.URLField(verbose_name="Ссылка")
    icon_class = models.CharField(max_length=50, blank=True, verbose_name="CSS класс иконки")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class ContactPageSettings(models.Model):
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Мета-заголовок")
    meta_description = models.TextField(blank=True, verbose_name="Мета-описание")
    show_breadcrumbs = models.BooleanField(default=True, verbose_name="Показывать хлебные крошки")
    show_organization_info = models.BooleanField(default=True, verbose_name="Показывать информацию об организации")
    
    class Meta:
        verbose_name = "Настройки страницы контактов"
        verbose_name_plural = "Настройки страницы контактов"
    
    def __str__(self):
        return "Настройки страницы контактов"
    
    def save(self, *args, **kwargs):
        # Разрешаем только одну запись настроек
        self.pk = 1
        super().save(*args, **kwargs)

class ContactHero(models.Model):
    title = models.CharField(max_length=200, verbose_name="Основной заголовок")
    subtitle = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='contacts/hero/', verbose_name="Изображение")
    show_breadcrumb = models.BooleanField(default=True, verbose_name="Показывать хлебные крошки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero раздел контактов"
        verbose_name_plural = "Hero разделы контактов"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Разрешаем только одну активную запись
        if self.is_active:
            ContactHero.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)