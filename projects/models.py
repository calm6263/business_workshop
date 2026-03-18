# projects/models.py
from django.db import models
from django.utils import timezone
from accounts.models import Company

class ProjectCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Категория проектов"
        verbose_name_plural = "Категории проектов"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECT_TYPES = [
        ('government', 'Госзаказы'),
        ('corporate', 'Корпоративные проекты'),
        ('grants', 'Гранты и финансирование'),
        ('contests', 'Конкурсные мероприятия'),
        ('youth', 'Молодежный ученый совет'),
        ('social', 'Социальные инициативы'),
        ('targeted', 'Целевое обучение'),
        ('patents', 'Патенты'),
        ('conferences', 'Конференции'),
    ]
    STATUS_CHOICES = [
        ('active', 'В разработке'),
        ('completed', 'Реализован'),
        ('planned', 'Планируется'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='projects'
    )

    title = models.CharField(max_length=500, verbose_name="Название проекта")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, verbose_name="Тип проекта")
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание проекта")
    short_description = models.TextField(max_length=500, verbose_name="Краткое описание")
    sidebar_title = models.CharField(max_length=500, blank=True, verbose_name="Заголовок боковой панели")
    image = models.ImageField(upload_to='projects/', verbose_name="Изображение")
    description_image = models.ImageField(upload_to='projects/description/', blank=True, null=True, verbose_name="Изображение над описанием")
    presentation_file = models.FileField(upload_to='projects/presentations/', blank=True, null=True, verbose_name="Файл презентации")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Бюджет")
    participants_count = models.IntegerField(default=0, verbose_name="Количество участников")
    results = models.TextField(blank=True, verbose_name="Результаты проекта")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый проект")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Руководитель'),
        ('member', 'Участник'),
        ('consultant', 'Консультант'),
        ('partner', 'Партнер'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='project_members'
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    name = models.CharField(max_length=200, verbose_name="ФИО участника")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Роль")
    organization = models.CharField(max_length=300, blank=True, verbose_name="Организация")
    position = models.CharField(max_length=200, blank=True, verbose_name="Должность")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Участник проекта"
        verbose_name_plural = "Участники проектов"

    def __str__(self):
        return f"{self.name} - {self.project.title}"


class ProjectPartner(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='project_partners'
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    name = models.CharField(max_length=200, verbose_name="Название партнера")
    logo = models.ImageField(upload_to='projects/partners/', blank=True, null=True, verbose_name="Логотип партнера")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    description = models.TextField(blank=True, verbose_name="Описание партнера")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Партнер проекта"
        verbose_name_plural = "Партнеры проектов"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.project.title}"


class ProjectSlide(models.Model):
    # يمكن أن تكون عامة (لجميع الشركات) أو خاصة، نعتبرها عامة.
    title = models.CharField(max_length=200, verbose_name="Заголовок слайда")
    image = models.ImageField(upload_to='project_slides/', verbose_name="Изображение слайда")
    description = models.TextField(blank=True, verbose_name="Описание слайда")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Слайд проектов"
        verbose_name_plural = "Слайды проектов"
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactRequest(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='contact_requests'
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Запрос обратной связи"
        verbose_name_plural = "Запросы обратной связи"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.project.title}"


class ProjectProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('reviewed', 'Рассмотрено'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='project_proposals'
    )

    unique_id = models.CharField(max_length=20, unique=True, verbose_name="Уникальный ID")
    title = models.CharField(max_length=500, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    organization = models.CharField(max_length=300, blank=True, verbose_name="Организация")
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Предполагаемый бюджет")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Срок реализации")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Предложение проекта"
        verbose_name_plural = "Предложения проектов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.unique_id} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        import random
        import string
        from django.utils import timezone
        timestamp = timezone.now().strftime("%y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"PP-{timestamp}-{random_str}"


class ProjectGallery(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='project_galleries'
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок изображения")
    image = models.ImageField(upload_to='project_gallery/', verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание изображения")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Связанный проект (необязательно)")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Галерея изображений"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.project.title if self.project else 'Общий'}"


class ProjectJoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('reviewed', 'Рассмотрено'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='project_join_requests'
    )

    unique_id = models.CharField(max_length=20, unique=True, verbose_name="Уникальный ID")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    person_type = models.CharField(max_length=20, choices=[('individual', 'Физическое лицо'), ('legal', 'Юридическое лицо')], verbose_name="Тип лица")
    # Данные физ. лица
    full_name_individual = models.CharField(max_length=200, blank=True, verbose_name="ФИО (физ. лицо)")
    phone_individual = models.CharField(max_length=20, blank=True, verbose_name="Телефон (физ. лицо)")
    email_individual = models.EmailField(blank=True, verbose_name="Email (физ. лицо)")
    address_individual = models.TextField(blank=True, verbose_name="Адрес (физ. лицо)")
    comments_individual = models.TextField(blank=True, verbose_name="Комментарии (физ. лицо)")
    # Данные юр. лица
    full_name_legal = models.CharField(max_length=200, blank=True, verbose_name="Ответственное лицо (юр. лицо)")
    phone_legal = models.CharField(max_length=20, blank=True, verbose_name="Телефон (юр. лицо)")
    email_legal = models.EmailField(blank=True, verbose_name="Email (юр. лицо)")
    company_name = models.CharField(max_length=300, blank=True, verbose_name="Название компании")
    inn = models.CharField(max_length=12, blank=True, verbose_name="ИНН")
    kpp = models.CharField(max_length=9, blank=True, verbose_name="КПП")
    legal_address = models.TextField(blank=True, verbose_name="Юридический адрес")
    comments_legal = models.TextField(blank=True, verbose_name="Комментарии (юр. лицо)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Запрос на вступление в проект"
        verbose_name_plural = "Запросы на вступление в проект"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.unique_id} - {self.project.title}"

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        import random
        import string
        from django.utils import timezone
        timestamp = timezone.now().strftime("%y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"PJR-{timestamp}-{random_str}"