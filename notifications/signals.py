# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.urls import reverse

from .models import Notification

User = get_user_model()

# Список всех моделей, которые представляют заявки (можно расширять)
APPLICATION_MODELS = [
    ('applicants', 'ApplicantApplication'),
    ('consultations', 'ConsultationRequest'),
    ('partners', 'PartnershipApplication'),
    ('single_window', 'ServiceRequest'),
    ('projects', 'ProjectProposal'),
    ('projects', 'ProjectJoinRequest'),
    ('schedule', 'ProgramApplication'),
    ('research', 'ConferenceRegistration'),
    ('press_center', 'PublicationRequest'),
    ('contact_form', 'ContactMessage'),          # <-- добавлено
]

def get_edit_url(instance):
    """
    Попытка построить URL для редактирования объекта с помощью reverse.
    Предполагается, что имя пути имеет вид dashboards:<model_name>_edit
    """
    model_name = instance._meta.model_name
    app_label = instance._meta.app_label
    # Сначала пробуем прямой путь (dashboards:<model_name>_edit)
    try:
        url = reverse(f'dashboards:{model_name}_edit', args=[instance.pk])
        return url
    except:
        pass
    # Если не получилось, пробуем dashboards:<app_label>_<model_name>_edit
    try:
        url = reverse(f'dashboards:{app_label}_{model_name}_edit', args=[instance.pk])
        return url
    except:
        pass
    # Если всё не удалось, возвращаем пустую строку
    return ''

def create_notification_for_admins(instance, verb, message, link=''):
    """Отправка уведомления всем администраторам"""
    admins = User.objects.filter(profile__user_type='admin')
    content_type = ContentType.objects.get_for_model(instance)
    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            actor=None,
            verb=verb,
            target_content_type=content_type,
            target_object_id=instance.pk,
            message=message,
            link=link,
            read=False
        )

def generate_notification(instance, created):
    if created:
        model_verbose = instance._meta.verbose_name
        message = f"Получена новая {model_verbose}"
        link = get_edit_url(instance)
        create_notification_for_admins(instance, 'created', message, link)

# Подключаем сигналы для всех перечисленных моделей
for app_label, model_name in APPLICATION_MODELS:
    try:
        model = apps.get_model(app_label, model_name)
        receiver(post_save, sender=model)(lambda sender, instance, created, **kwargs: generate_notification(instance, created))
    except LookupError:
        pass