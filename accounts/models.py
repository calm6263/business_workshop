# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserType(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    REGULAR = 'regular', 'Обычный пользователь'
    TEACHER = 'teacher', 'Преподаватель'
    STUDENT = 'student', 'Студент'
    COMPANY = 'company', 'Компания'

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название компании")
    registration_number = models.CharField(max_length=50, blank=True, verbose_name="Регистрационный номер")
    address = models.TextField(blank=True, verbose_name="Адрес")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.REGULAR,
        verbose_name="Тип пользователя"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Компания (для аккаунтов компаний и сотрудников)",
        related_name='profiles'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# Signal to auto-create Profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            user_type = UserType.ADMIN
        else:
            user_type = UserType.REGULAR
        Profile.objects.create(user=instance, user_type=user_type)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()