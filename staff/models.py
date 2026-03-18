# staff/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from schedule.models import ScheduleProgram
from departments.models import Department
from accounts.models import Company

class TeamMember(models.Model):
    MEMBER_TYPES = [
        ('teacher', 'Преподаватель'),
        ('staff', 'Сотрудник'),
        ('educational_council', 'Учебный совет'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='team_members'
    )

    name = models.CharField(max_length=200, verbose_name="Имя")
    image = models.ImageField(upload_to='team/', verbose_name="Фото")
    position = models.TextField(verbose_name="Должность")
    description = models.TextField(blank=True, verbose_name="Описание")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    qualifications = models.TextField(blank=True, verbose_name="Квалификации и образование")
    experience = models.TextField(blank=True, verbose_name="Опыт работы")
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPES, verbose_name="Тип")
    departments = models.ManyToManyField(Department, related_name='team_members', blank=True, verbose_name="Отделения")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Члены команды"
        ordering = ['member_type', 'order', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_member_type_display()}"

    def get_absolute_url(self):
        return reverse('staff:team_member_detail', kwargs={'pk': self.pk})


class TeacherProgram(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        null=True, blank=True,
        related_name='teacher_programs'
    )

    teacher = models.ForeignKey(TeamMember, on_delete=models.CASCADE, verbose_name="Преподаватель", limit_choices_to={'member_type': 'teacher'})
    program = models.ForeignKey(ScheduleProgram, on_delete=models.CASCADE, verbose_name="Программа")
    role = models.CharField(max_length=100, verbose_name="Роль преподавателя")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Программа преподавателя"
        verbose_name_plural = "Программы преподавателей"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.teacher.name} - {self.program.title}"


class PageHero(models.Model):
    PAGE_CHOICES = [
        ('teachers_staff', 'Преподаватели и сотрудники'),
    ]
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, verbose_name="Страница")
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок")
    subtitle = models.TextField(blank=True, verbose_name="Подзаголовок")
    image = models.ImageField(upload_to='hero_images/', verbose_name="Изображение героя")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Изображение героя для страницы"
        verbose_name_plural = "Изображения героев для страниц"
        ordering = ['page']

    def __str__(self):
        return self.get_page_display()