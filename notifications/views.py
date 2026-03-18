# notifications/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Notification, ActivityLog

User = get_user_model()


# ---------- API для уведомлений (AJAX) ----------
@login_required
def api_unread_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False, archived=False)[:10]
    data = [{
        'id': n.id,
        'message': n.message,
        'link': n.link,
        'created_at': n.created_at.strftime('%d.%m.%Y %H:%M'),
        'verb': n.verb,
    } for n in notifications]
    return JsonResponse({
        'unread_count': Notification.objects.filter(recipient=request.user, read=False, archived=False).count(),
        'notifications': data
    })


@login_required
@require_POST
def api_mark_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_mark_all_read(request):
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_archive(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.archived = True
    notification.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_unarchive(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.archived = False
    notification.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_delete(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_archive_all_read(request):
    Notification.objects.filter(recipient=request.user, read=True, archived=False).update(archived=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def api_delete_all_archived(request):
    Notification.objects.filter(recipient=request.user, archived=True).delete()
    return JsonResponse({'status': 'ok'})


# ---------- Страница со всеми уведомлениями ----------
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('archived') == '1':
            return Notification.objects.filter(recipient=self.request.user, archived=True)
        return Notification.objects.filter(recipient=self.request.user, archived=False)


# ---------- Страница журнала действий (для администраторов и суперпользователей) ----------
class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'notifications/activity_log_list.html'
    context_object_name = 'logs'
    paginate_by = 15  # Изменено на 15

    def get_queryset(self):
        user = self.request.user
        # Проверка прав доступа
        if not (user.is_superuser or (hasattr(user, 'profile') and user.profile.user_type == 'admin')):
            return ActivityLog.objects.none()

        # Базовый queryset
        queryset = ActivityLog.objects.all().select_related('user', 'content_type')

        # Фильтр по действию (action)
        action = self.request.GET.get('action')
        if action and action != 'all':
            queryset = queryset.filter(action=action)

        # Фильтр по пользователю
        user_id = self.request.GET.get('user')
        if user_id and user_id.isdigit():
            queryset = queryset.filter(user_id=int(user_id))

        # Фильтр по дате начала
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(timestamp__date__gte=date_from)

        # Фильтр по дате окончания
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(timestamp__date__lte=date_to)

        # Фильтр по модели (app_label.model_name)
        model_filter = self.request.GET.get('model')
        if model_filter:
            try:
                app_label, model_name = model_filter.split('.')
                from django.contrib.contenttypes.models import ContentType
                content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
                queryset = queryset.filter(content_type=content_type)
            except (ValueError, ContentType.DoesNotExist):
                pass

        # Поиск по объекту (object_repr)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(object_repr__icontains=search) | Q(user__username__icontains=search))

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Список всех действий для фильтра
        context['action_choices'] = [
            ('all', 'Все действия'),
            ('create', 'Создание'),
            ('update', 'Изменение'),
            ('delete', 'Удаление'),
        ]

        # Список всех пользователей, которые совершали действия
        context['users'] = User.objects.filter(activitylog__isnull=False).distinct().order_by('username')

        # Список всех моделей, по которым есть записи
        content_type_ids = ActivityLog.objects.values_list('content_type', flat=True).distinct()
        from django.contrib.contenttypes.models import ContentType
        content_types = ContentType.objects.filter(id__in=content_type_ids)
        model_list = []
        for ct in content_types:
            model_list.append({
                'value': f"{ct.app_label}.{ct.model}",
                'label': f"{ct.app_label} / {ct.model}",
            })
        context['model_choices'] = model_list

        # Сохраняем текущие параметры фильтра для отображения в шаблоне
        context['filter_action'] = self.request.GET.get('action', '')
        context['filter_user'] = self.request.GET.get('user', '')
        context['filter_date_from'] = self.request.GET.get('date_from', '')
        context['filter_date_to'] = self.request.GET.get('date_to', '')
        context['filter_model'] = self.request.GET.get('model', '')
        context['filter_search'] = self.request.GET.get('search', '')

        return context