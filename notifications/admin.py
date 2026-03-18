# notifications/admin.py
import csv
import json
from django.http import HttpResponse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .models import Notification, ActivityLog


class ExportCsvMixin:
    """
    Mixin لإضافة إجراء تصدير CSV إلى نموذج المسؤول.
    """
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)

        # كتابة رؤوس الأعمدة
        writer.writerow(field_names)

        # كتابة البيانات
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                if field == 'changes' and value:
                    # تحويل JSON إلى نص منسق
                    row.append(json.dumps(value, ensure_ascii=False, indent=2))
                else:
                    row.append(str(value) if value is not None else '')
            writer.writerow(row)

        return response

    export_as_csv.short_description = "📥 Экспорт выбранных в CSV"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('recipient', 'verb', 'message_short', 'read', 'archived', 'created_at')
    list_filter = ('read', 'archived', 'verb', 'created_at')
    search_fields = ('recipient__username', 'message')
    readonly_fields = ('recipient', 'actor', 'verb', 'target_content_type',
                       'target_object_id', 'message', 'link', 'created_at')
    actions = ['export_as_csv']

    def message_short(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_short.short_description = "Сообщение"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'action', 'object_repr', 'app_model', 'timestamp')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('user__username', 'object_repr', 'changes')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'object_repr', 'changes_display', 'timestamp')
    actions = ['export_as_csv']

    def app_model(self, obj):
        app_label = obj.content_type.app_label
        model_name = obj.content_type.model
        return f"{app_label} / {model_name}"
    app_model.short_description = "Приложение / Модель"

    def changes_display(self, obj):
        if not obj.changes:
            return "-"

        changes = obj.changes
        html = '<div style="max-width:400px; max-height:200px; overflow:auto; background:#f8f9fa; padding:8px; border-radius:4px;">'

        # عرض المعلومات الأساسية
        meta = changes.get('_meta', {})
        if meta:
            app_label = escape(meta.get('app_label', ''))
            model_name = escape(meta.get('model_name', ''))
            obj_repr = escape(meta.get('object_repr', ''))
            html += f'<div><strong>Объект:</strong> {obj_repr} ({app_label} / {model_name})</div>'

        # عرض التغييرات الحقلية
        field_changes = {k: v for k, v in changes.items() if not k.startswith('_')}
        if field_changes:
            html += '<div style="margin-top:8px;"><strong>Изменения полей:</strong></div>'
            html += '<table style="width:100%; border-collapse:collapse; font-size:0.9rem;">'
            html += '<tr><th style="text-align:left; border-bottom:1px solid #ddd;">Поле</th><th style="text-align:left; border-bottom:1px solid #ddd;">Старое значение</th><th style="text-align:left; border-bottom:1px solid #ddd;">Новое значение</th></tr>'

            # قاموس ترجمة أسماء الحقول إلى الروسية (يمكن توسيعه) - تم حذفه للاختصار، لكن يمكن إضافته لاحقاً
            field_translations = {
                'title': 'Заголовок',
                'image': 'Изображение',
                'description': 'Описание',
                'is_active': 'Активно',
                'order': 'Порядок',
                'name': 'Название',
                # ... остальные переводы
            }

            for field, values in field_changes.items():
                field_ru = escape(field_translations.get(field, field))
                old_val = escape(str(values.get('old', ''))) if values.get('old') is not None else ''
                new_val = escape(str(values.get('new', ''))) if values.get('new') is not None else ''
                html += f'<tr><td style="padding:4px 0; border-bottom:1px solid #eee;"><strong>{field_ru}</strong></td>'
                html += f'<td style="padding:4px 0; border-bottom:1px solid #eee;">{old_val}</td>'
                html += f'<td style="padding:4px 0; border-bottom:1px solid #eee;">{new_val}</td></tr>'

            html += '</table>'

        html += '</div>'
        return mark_safe(html)

    changes_display.short_description = "Детали изменений"

    # ---------- تقييد الوصول إلى المستخدمين الفائقين فقط ----------
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False