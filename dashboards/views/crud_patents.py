# dashboards/views/crud_patents.py
from django.urls import reverse_lazy
from patents.models import PatentImage
from .mixins import (
    BaseAdminListView,
    BaseAdminCreateView,
    BaseAdminUpdateView,
    BaseAdminDeleteView
)

class PatentImageListView(BaseAdminListView):
    """Список изображений патентов"""
    model = PatentImage
    template_name = 'dashboards/crud/patents/patentimage_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        # Сортировка по order, затем по дате создания
        return super().get_queryset().order_by('order', 'created_at')


class PatentImageCreateView(BaseAdminCreateView):
    """Добавление нового изображения патента"""
    model = PatentImage
    fields = ['title', 'image', 'caption', 'order', 'is_active']
    template_name = 'dashboards/crud/patents/patentimage_form.html'
    success_url = reverse_lazy('dashboards:patentimage_list')
    success_message = "Изображение успешно добавлено"


class PatentImageUpdateView(BaseAdminUpdateView):
    """Редактирование изображения патента"""
    model = PatentImage
    fields = ['title', 'image', 'caption', 'order', 'is_active']
    template_name = 'dashboards/crud/patents/patentimage_form.html'
    success_url = reverse_lazy('dashboards:patentimage_list')
    success_message = "Изображение успешно обновлено"


class PatentImageDeleteView(BaseAdminDeleteView):
    """Удаление изображения патента"""
    model = PatentImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:patentimage_list')
    success_message = "Изображение успешно удалено"