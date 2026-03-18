# dashboards/views/crud_contact_form.py
from django.urls import reverse_lazy
from contact_form.models import ContactMessage
from .mixins import BaseAdminListView, BaseAdminUpdateView, BaseAdminDeleteView

class ContactMessageListView(BaseAdminListView):
    """
    Список всех сообщений обратной связи.
    """
    model = ContactMessage
    template_name = 'dashboards/crud/contact_form/contactmessage_list.html'
    context_object_name = 'items'
    paginate_by = 20
    ordering = ['-created_at']

    def get_queryset(self):
        # При необходимости можно добавить фильтрацию
        return super().get_queryset()


class ContactMessageUpdateView(BaseAdminUpdateView):
    """
    Редактирование сообщения (разрешено только поле is_read).
    """
    model = ContactMessage
    fields = ['is_read']   # только отметка о прочтении
    template_name = 'dashboards/crud/contact_form/contactmessage_form.html'
    success_url = reverse_lazy('dashboards:contactmessage_list')
    success_message = "Сообщение успешно обновлено"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Делаем все поля, кроме is_read, только для чтения
        readonly_fields = ['name', 'email', 'message', 'created_at', 'client_ip', 'user_agent']
        for field in readonly_fields:
            if field in form.fields:
                form.fields[field].disabled = True
        return form


class ContactMessageDeleteView(BaseAdminDeleteView):
    """
    Удаление сообщения.
    """
    model = ContactMessage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:contactmessage_list')
    success_message = "Сообщение удалено"