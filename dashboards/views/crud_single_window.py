from django.urls import reverse_lazy
from django.http import Http404

from single_window.models import BasicInfo, Slider, FAQ, ServiceRequest
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- BasicInfo (Singleton) ----------------------
class BasicInfoListView(BaseAdminListView):
    model = BasicInfo
    template_name = 'dashboards/crud/single_window/basicinfo_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return BasicInfo.objects.all()[:1]

class BasicInfoCreateView(BaseAdminCreateView):
    model = BasicInfo
    fields = '__all__'
    template_name = 'dashboards/crud/single_window/basicinfo_form.html'
    success_url = reverse_lazy('dashboards:basicinfo_list')
    success_message = "Основные сведения успешно созданы"

    def dispatch(self, request, *args, **kwargs):
        if BasicInfo.objects.exists():
            raise Http404("Основные сведения уже существуют. Вы можете только редактировать их.")
        return super().dispatch(request, *args, **kwargs)

class BasicInfoUpdateView(BaseAdminUpdateView):
    model = BasicInfo
    fields = '__all__'
    template_name = 'dashboards/crud/single_window/basicinfo_form.html'
    success_url = reverse_lazy('dashboards:basicinfo_list')
    success_message = "Основные сведения успешно обновлены"

class BasicInfoDeleteView(BaseAdminDeleteView):
    model = BasicInfo
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:basicinfo_list')
    success_message = "Основные сведения удалены"

# ---------------------- Slider ----------------------
class SliderListView(BaseAdminListView):
    model = Slider
    template_name = 'dashboards/crud/single_window/slider_list.html'
    context_object_name = 'items'
    ordering = ['order']

class SliderCreateView(BaseAdminCreateView):
    model = Slider
    fields = ['title', 'subtitle', 'description', 'image', 'link', 'link_text', 'is_active', 'order']
    template_name = 'dashboards/crud/single_window/slider_form.html'
    success_url = reverse_lazy('dashboards:slider_list')
    success_message = "Слайд добавлен"

class SliderUpdateView(BaseAdminUpdateView):
    model = Slider
    fields = ['title', 'subtitle', 'description', 'image', 'link', 'link_text', 'is_active', 'order']
    template_name = 'dashboards/crud/single_window/slider_form.html'
    success_url = reverse_lazy('dashboards:slider_list')
    success_message = "Слайд обновлен"

class SliderDeleteView(BaseAdminDeleteView):
    model = Slider
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:slider_list')
    success_message = "Слайд удален"

# ---------------------- FAQ ----------------------
class FAQListView(BaseAdminListView):
    model = FAQ
    template_name = 'dashboards/crud/single_window/faq_list.html'
    context_object_name = 'items'
    ordering = ['service', 'question_number']

class FAQCreateView(BaseAdminCreateView):
    model = FAQ
    fields = ['service', 'question_number', 'question', 'answer', 'is_active']
    template_name = 'dashboards/crud/single_window/faq_form.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ добавлен"

class FAQUpdateView(BaseAdminUpdateView):
    model = FAQ
    fields = ['service', 'question_number', 'question', 'answer', 'is_active']
    template_name = 'dashboards/crud/single_window/faq_form.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ обновлен"

class FAQDeleteView(BaseAdminDeleteView):
    model = FAQ
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ удален"

# ---------------------- ServiceRequest ----------------------
class ServiceRequestListView(BaseAdminListView):
    model = ServiceRequest
    template_name = 'dashboards/crud/single_window/servicerequest_list.html'
    context_object_name = 'items'
    paginate_by = 20
    ordering = ['-created_at']

class ServiceRequestUpdateView(BaseAdminUpdateView):
    model = ServiceRequest
    fields = ['status', 'admin_notes']
    template_name = 'dashboards/crud/single_window/servicerequest_form.html'
    success_url = reverse_lazy('dashboards:servicerequest_list')
    success_message = "Заявка обновлена"

class ServiceRequestDeleteView(BaseAdminDeleteView):
    model = ServiceRequest
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:servicerequest_list')
    success_message = "Заявка удалена"