from django.urls import reverse_lazy
from django.http import Http404

from press_center.models import PressCenterPage, PressCenterImage, PublicationRequest
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- PressCenterPage (Singleton) ----------------------
class PressCenterPageListView(BaseAdminListView):
    model = PressCenterPage
    template_name = 'dashboards/crud/press_center/presscenterpage_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return PressCenterPage.objects.all()[:1]

class PressCenterPageCreateView(BaseAdminCreateView):
    model = PressCenterPage
    fields = ['title', 'background_image', 'description', 'publication_rules_file', 'is_active']
    template_name = 'dashboards/crud/press_center/presscenterpage_form.html'
    success_url = reverse_lazy('dashboards:presscenterpage_list')
    success_message = "Страница успешно создана"

    def dispatch(self, request, *args, **kwargs):
        if PressCenterPage.objects.exists():
            raise Http404("Страница уже существует. Вы можете только редактировать её.")
        return super().dispatch(request, *args, **kwargs)

class PressCenterPageUpdateView(BaseAdminUpdateView):
    model = PressCenterPage
    fields = ['title', 'background_image', 'description', 'publication_rules_file', 'is_active']
    template_name = 'dashboards/crud/press_center/presscenterpage_form.html'
    success_url = reverse_lazy('dashboards:presscenterpage_list')
    success_message = "Страница успешно обновлена"

class PressCenterPageDeleteView(BaseAdminDeleteView):
    model = PressCenterPage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:presscenterpage_list')
    success_message = "Страница удалена"

# ---------------------- PressCenterImage ----------------------
class PressCenterImageListView(BaseAdminListView):
    model = PressCenterImage
    template_name = 'dashboards/crud/press_center/presscenterimage_list.html'
    context_object_name = 'items'
    ordering = ['order']

class PressCenterImageCreateView(BaseAdminCreateView):
    model = PressCenterImage
    fields = ['press_center', 'image', 'caption', 'order']
    template_name = 'dashboards/crud/press_center/presscenterimage_form.html'
    success_url = reverse_lazy('dashboards:presscenterimage_list')
    success_message = "Изображение добавлено"

class PressCenterImageUpdateView(BaseAdminUpdateView):
    model = PressCenterImage
    fields = ['press_center', 'image', 'caption', 'order']
    template_name = 'dashboards/crud/press_center/presscenterimage_form.html'
    success_url = reverse_lazy('dashboards:presscenterimage_list')
    success_message = "Изображение обновлено"

class PressCenterImageDeleteView(BaseAdminDeleteView):
    model = PressCenterImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:presscenterimage_list')
    success_message = "Изображение удалено"

# ---------------------- PublicationRequest ----------------------
class PublicationRequestListView(BaseAdminListView):
    model = PublicationRequest
    template_name = 'dashboards/crud/press_center/publicationrequest_list.html'
    context_object_name = 'items'
    paginate_by = 20
    ordering = ['-created_at']

class PublicationRequestUpdateView(BaseAdminUpdateView):
    model = PublicationRequest
    fields = ['status']
    template_name = 'dashboards/crud/press_center/publicationrequest_form.html'
    success_url = reverse_lazy('dashboards:publicationrequest_list')
    success_message = "Статус заявки обновлен"

class PublicationRequestDeleteView(BaseAdminDeleteView):
    model = PublicationRequest
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:publicationrequest_list')
    success_message = "Заявка удалена"