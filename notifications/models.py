# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Notification(models.Model):
    """
    Модель уведомления для пользователей (в основном для администраторов).
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Получатель"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='actor_notifications',
        verbose_name="Исполнитель"
    )
    verb = models.CharField(max_length=255, verbose_name="Действие")  # например "создал", "обновил"
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    message = models.TextField(verbose_name="Сообщение")
    link = models.CharField(max_length=500, blank=True, verbose_name="Ссылка")
    read = models.BooleanField(default=False, verbose_name="Прочитано")
    archived = models.BooleanField(default=False, verbose_name="В архиве")  # новое поле
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.recipient} - {self.verb} - {self.created_at}"


class ActivityLog(models.Model):
    """
    Журнал действий администраторов в панели управления.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь"
    )
    action = models.CharField(max_length=50, verbose_name="Действие")  # create, update, delete
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200, verbose_name="Объект")
    changes = models.JSONField(null=True, blank=True, verbose_name="Изменения")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Время")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Запись журнала"
        verbose_name_plural = "Журнал действий"