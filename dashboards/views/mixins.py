# dashboards/views/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.forms import FileField, ImageField
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.contenttypes.models import ContentType
from notifications.models import ActivityLog
import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt',
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
    '.zip', '.rar', '.7z',
    '.csv', '.xml', '.json'
}

def validate_file_extension(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Недопустимый тип файла. Разрешены: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

class FileValidationMixin:
    def form_valid(self, form):
        for field_name, field in form.fields.items():
            if isinstance(field, (FileField, ImageField)):
                uploaded_file = form.cleaned_data.get(field_name)
                if uploaded_file and hasattr(uploaded_file, 'size'):
                    if uploaded_file.size > MAX_FILE_SIZE:
                        form.add_error(field_name, f"Файл слишком большой. Максимальный размер {MAX_FILE_SIZE // (1024*1024)} МБ.")
                        return self.form_invalid(form)
                    try:
                        validate_file_extension(uploaded_file.name)
                    except ValidationError as e:
                        form.add_error(field_name, e.message)
                        return self.form_invalid(form)
                    if isinstance(field, ImageField) and hasattr(uploaded_file, 'read'):
                        try:
                            img = Image.open(uploaded_file)
                            img.verify()
                        except Exception:
                            form.add_error(field_name, "Файл повреждён или не является изображением.")
                            return self.form_invalid(form)
        return super().form_valid(form)

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('accounts:login')

    def test_func(self):
        user = self.request.user
        return (user.is_authenticated and
                hasattr(user, 'profile') and
                user.profile.user_type == 'admin')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "У вас недостаточно прав для доступа к этой странице.")
            return redirect(reverse_lazy('dashboards:dashboard'))
        return super().handle_no_permission()


class LoggingMixin:
    def get_changes(self, instance, form=None):
        changes = {}
        meta_info = {
            'app_label': instance._meta.app_label,
            'model_name': instance._meta.model_name,
            'object_id': instance.pk,
            'object_repr': str(instance),
        }
        if form and form.changed_data:
            if instance.pk:
                try:
                    original = instance.__class__.objects.get(pk=instance.pk)
                    for field in form.changed_data:
                        if field in form.cleaned_data:
                            old_value = getattr(original, field)
                            new_value = form.cleaned_data[field]
                            changes[field] = {
                                'old': str(old_value) if old_value is not None else None,
                                'new': str(new_value) if new_value is not None else None,
                            }
                except instance.__class__.DoesNotExist:
                    pass
        elif not instance.pk and form:
            for field, value in form.cleaned_data.items():
                if value is not None:
                    changes[field] = {'new': str(value)}
        changes['_meta'] = meta_info
        return changes

    def log_activity(self, action, instance, form=None):
        try:
            changes = self.get_changes(instance, form)
            ActivityLog.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                action=action,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
                object_repr=str(instance),
                changes=changes
            )
        except Exception as e:
            logger.error(f"Ошибка записи действия (action={action}, instance={instance}): {e}", exc_info=True)


# ========== Mixin جديد للتصفية حسب الشركة ==========
class CompanyFilterMixin:
    """
    Mixin لتصفية queryset بناءً على الشركة إذا كان المستخدم من نوع company.
    يفترض وجود حقل 'company' في النموذج.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.user_type == 'company' and user.profile.company:
            # إذا كان المستخدم من شركة، نقوم بتصفية النتائج حسب شركته
            if hasattr(queryset.model, 'company'):
                return queryset.filter(company=user.profile.company)
        # المستخدم admin يرى الكل
        return queryset


@method_decorator(never_cache, name='dispatch')
class BaseCRUDListView(AdminRequiredMixin, CompanyFilterMixin, ListView):
    paginate_by = 20
    context_object_name = 'items'

    def get_queryset(self):
        return super().get_queryset().order_by('-id')


@method_decorator(never_cache, name='dispatch')
class BaseCRUDCreateView(AdminRequiredMixin, SuccessMessageMixin, FileValidationMixin, CreateView, LoggingMixin):
    success_message = "Запись успешно создана"

    def form_valid(self, form):
        # إذا كان المستخدم من شركة، نقوم بتعيين company تلقائياً
        if hasattr(self.request.user, 'profile') and self.request.user.profile.user_type == 'company':
            if hasattr(form.instance, 'company'):
                form.instance.company = self.request.user.profile.company
        response = super().form_valid(form)
        self.log_activity('create', self.object, form)
        return response


@method_decorator(never_cache, name='dispatch')
class BaseCRUDUpdateView(AdminRequiredMixin, SuccessMessageMixin, FileValidationMixin, UpdateView, LoggingMixin):
    success_message = "Запись успешно обновлена"

    def get_queryset(self):
        # تأكد من أن المستخدم لا يمكنه تعديل عناصر ليست من شركته
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.user_type == 'company' and user.profile.company:
            if hasattr(qs.model, 'company'):
                return qs.filter(company=user.profile.company)
        return qs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_activity('update', self.object, form)
        return response


@method_decorator(never_cache, name='dispatch')
class BaseCRUDDeleteView(AdminRequiredMixin, DeleteView, LoggingMixin):
    template_name = 'dashboards/crud/confirm_delete.html'
    success_message = "Запись успешно удалена"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.user_type == 'company' and user.profile.company:
            if hasattr(qs.model, 'company'):
                return qs.filter(company=user.profile.company)
        return qs

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.log_activity('delete', self.object)
        except Exception as e:
            logger.error(f"Ошибка при записи удаления: {e}", exc_info=True)
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


BaseAdminCreateView = BaseCRUDCreateView
BaseAdminUpdateView = BaseCRUDUpdateView
BaseAdminListView = BaseCRUDListView
BaseAdminDeleteView = BaseCRUDDeleteView