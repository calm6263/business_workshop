# schedule/models.py
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.models import Company

try:
    from departments.models import Department
except ImportError:
    Department = None


class ScheduleProgram(models.Model):
    PROGRAM_TYPES = [
        ('professional_retraining', 'Профессиональная переподготовка'),
        ('qualification_upgrade', 'Повышение квалификации'),
        ('seminar', 'Семинар'),
        ('training', 'Тренинг'),
        ('other', 'Другое'),
    ]
    FORMAT_CHOICES = [
        ('offline', 'Очно'),
        ('blended', 'Очно-заочно'),
        ('correspondence', 'Заочно'),
        ('online', 'Онлайн'),
    ]
    CERTIFICATION_TYPES = [
        ('certified', 'Сертифицированные программы'),
        ('diploma', 'Дипломированные программы'),
        ('attestation', 'Удостоверительные программы'),
        ('none', 'Без сертификации'),
    ]
    ENROLLMENT_STATUS_CHOICES = [
        ('open', 'Набор открыт'),
        ('closed', 'Набор закрыт'),
        ('upcoming', 'Предстоящий'),
        ('archive', 'Архив'),
        ('on_request', 'По запросу'),
        ('postponed', 'Перенесен на'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='schedule_programs'
    )

    title = models.CharField(max_length=500, verbose_name="Название программы")
    program_type = models.CharField(max_length=50, choices=PROGRAM_TYPES, verbose_name="Тип программы")
    certification_type = models.CharField(
        max_length=50,
        choices=CERTIFICATION_TYPES,
        default='none',
        verbose_name="Тип сертификации"
    )
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='offline', verbose_name="Формат")
    detailed_description = models.TextField(blank=True, verbose_name="Подробное описание")
    schedule_description = models.TextField(
        blank=True,
        verbose_name="Описание расписания",
        help_text="Текст для раздела 'Расписание занятий'. Если оставить пустым, будет использован текст по умолчанию."
    )
    admission_requirements = models.TextField(
        blank=True,
        verbose_name="Требования к слушателям и документы для поступления",
        help_text="Оставьте пустым, чтобы использовать стандартный текст"
    )
    target_audience = models.TextField(
        blank=True,
        verbose_name="Целевая аудитория (каждый пункт с новой строки)",
        help_text="Введите каждый пункт списка с новой строки. Если оставить пустым, будет использован текст по умолчанию."
    )
    side_image = models.ImageField(upload_to='schedule/side_images/', blank=True, null=True, verbose_name="Боковое изображение")
    diploma_image_1 = models.ImageField(
        upload_to='schedule/diplomas/',
        blank=True, null=True,
        verbose_name="Дипломное изображение 1"
    )
    diploma_image_2 = models.ImageField(
        upload_to='schedule/diplomas/',
        blank=True, null=True,
        verbose_name="Дипломное изображение 2"
    )
    start_date = models.DateField(
        verbose_name="Дата начала",
        null=True, blank=True
    )
    end_date = models.DateField(
        verbose_name="Дата окончания",
        null=True, blank=True
    )
    duration = models.CharField(max_length=100, verbose_name="Длительность", blank=True, null=True)
    duration_hours = models.IntegerField(default=0, verbose_name="Количество часов")
    image = models.ImageField(upload_to='schedule/', blank=True, null=True, verbose_name="Изображение")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        null=True, blank=True
    )
    enrollment_status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default='open',
        verbose_name="Статус набора"
    )
    postponed_date = models.DateField(
        null=True, blank=True,
        verbose_name="Перенесено на дату",
        help_text="Укажите дату, на которую перенесена программа (для статуса «Перенесен на»)"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name='programs',
        verbose_name="Отделение",
        null=True, blank=True
    )
    schedule_document = models.FileField(
        upload_to='schedule/schedule_documents/',
        verbose_name="Файл расписания программ обучения",
        blank=True, null=True,
        help_text="Загрузите файл расписания программ обучения (PDF, Word, Excel)"
    )
    admission_form_document = models.FileField(
        upload_to='schedule/admission_forms/',
        verbose_name="Образец заявления на поступление",
        blank=True, null=True,
        help_text="Загрузите образец заявления на поступление (PDF, Word, Excel)"
    )

    class Meta:
        verbose_name = "Программа расписания"
        verbose_name_plural = "Программы расписания"
        ordering = ['start_date', 'order']

    def clean(self):
        if not self.start_date:
            raise ValidationError({'start_date': 'Дата начала обязательна для программ расписания'})
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'Дата окончания не может быть раньше даты начала'})
        if self.enrollment_status != 'postponed':
            self.postponed_date = None

    def calculate_duration(self):
        if self.start_date and self.end_date and self.end_date >= self.start_date:
            delta = relativedelta(self.end_date, self.start_date)
            months = delta.months
            years = delta.years
            days = delta.days
            total_months = years * 12 + months
            duration_parts = []
            if total_months > 0:
                if total_months == 1:
                    duration_parts.append("1 месяц")
                elif total_months < 5:
                    duration_parts.append(f"{total_months} месяца")
                else:
                    duration_parts.append(f"{total_months} месяцев")
            if days > 0:
                if days == 1:
                    duration_parts.append("1 день")
                elif days < 5:
                    duration_parts.append(f"{days} дня")
                else:
                    duration_parts.append(f"{days} дней")
            if duration_parts:
                return " ".join(duration_parts)
            else:
                return "Менее дня"
        return None

    def get_schedule_description_display(self):
        if self.schedule_description:
            return self.schedule_description
        return "Режим занятий (вечерний формат) - три раза в неделю с 18:55 до 22:00."

    def get_admission_requirements_display(self):
        if self.admission_requirements:
            return self.admission_requirements
        return """Требования к слушателям
К освоению программы допускаются лица, имеющие или получающие высшее/среднее профессиональное образование

Документы для поступления
Копия диплома о высшем или среднем профессиональном образовании с приложением или справка с места учебы (для студентов)
Паспорт: 2-3 страница (фото) и страницы с регистрацией
Две фотографии 3х4см + 1 в электронном виде (for пропуска)
СНИЛС"""

    def get_target_audience_display(self):
        if self.target_audience:
            return self.target_audience
        return (
            "Работаете в какой-то из смежных областей (психолог, бизнес-тренер, "
            "бизнес-консультант и т.д.) и стремитесь стать более востребованным специалистом\n"
            "Ищете новые возможности для развития своего бизнеса и видите их в применении "
            "коучингового подхода\n"
            "Работаете в сфере HR и готовы использовать инструменты коучинга в "
            "профессиональной деятельности\n"
            "Занимаете руководящую должность, и для вас важно эффективно выстраивать "
            "коммуникацию с сотрудниками"
        )

    def get_target_audience_list(self):
        text = self.get_target_audience_display()
        return [line.strip() for line in text.split('\n') if line.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ScheduleProgram.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if not self.start_date:
            self.start_date = date.today()
        if self.start_date and self.end_date and not self.duration:
            calculated_duration = self.calculate_duration()
            if calculated_duration:
                self.duration = calculated_duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_date} - {self.title}"


class CurriculumModule(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='curriculum_modules'
    )

    program = models.ForeignKey(ScheduleProgram, on_delete=models.CASCADE, related_name='curriculum_modules', verbose_name="Программа")
    title = models.CharField(max_length=500, verbose_name="Название модуля")
    description = models.TextField(blank=True, verbose_name="Описание модуля")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Модуль учебной программы"
        verbose_name_plural = "Модули учебной программы"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.program.title} - {self.title}"


class CurriculumDocument(models.Model):
    DOCUMENT_TYPES = [
        ('word', 'Word документ'),
        ('excel', 'Excel документ'),
        ('pdf', 'PDF документ'),
        ('other', 'Другой документ'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='curriculum_documents'
    )

    program = models.ForeignKey(ScheduleProgram, on_delete=models.CASCADE, related_name='curriculum_documents', verbose_name="Программа")
    title = models.CharField(max_length=500, verbose_name="Название документа")
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, default='pdf', verbose_name="Тип документа")
    file = models.FileField(upload_to='schedule/curriculum_documents/', verbose_name="Файл")
    description = models.TextField(blank=True, verbose_name="Описание документа")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Документ программы обучения"
        verbose_name_plural = "Документы программ обучения"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.program.title} - {self.title}"


class ProgramApplication(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='program_applications'
    )

    program = models.ForeignKey(ScheduleProgram, on_delete=models.CASCADE, verbose_name="Программа")
    application_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")
    contact_name = models.CharField(max_length=255, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    additional_info = models.TextField(blank=True, verbose_name="Дополнительные пожелания")
    agreement = models.BooleanField(default=False, verbose_name="Согласие с условиями")
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS, default='pending', verbose_name="Статус заявки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка на обучение"
        verbose_name_plural = "Заявки на обучение"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.application_number:
            from datetime import datetime
            base_number = datetime.now().strftime("%Y%m%d%H%M%S")
            counter = 1
            while ProgramApplication.objects.filter(application_number=f"APP-{base_number}-{counter:02d}").exists():
                counter += 1
            self.application_number = f"APP-{base_number}-{counter:02d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} - {self.contact_name}"


class ScheduleSliderImage(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='schedule_slider_images'
    )

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='schedule/slider/', verbose_name="Изображение слайдера")
    link = models.URLField(blank=True, verbose_name="Ссылка")
    link_text = models.CharField(max_length=100, blank=True, verbose_name="Текст ссылки")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение слайдера расписания"
        verbose_name_plural = "Изображения слайдера расписания"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class CalendarSliderImage(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='calendar_slider_images'
    )

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='schedule/calendar_slider/', verbose_name="Изображение слайдера")
    link = models.URLField(blank=True, verbose_name="Ссылка")
    link_text = models.CharField(max_length=100, blank=True, verbose_name="Текст ссылки")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Изображение слайдера календаря"
        verbose_name_plural = "Изображения слайдера календаря"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title