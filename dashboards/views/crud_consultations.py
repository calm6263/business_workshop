from django.urls import reverse_lazy

from consultations.models import ConsultationRequest, HeroSlide, FAQ, SuccessPageImage
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ConsultationRequest ----------------------
class ConsultationRequestListView(BaseAdminListView):
    model = ConsultationRequest
    template_name = 'dashboards/crud/consultations/consultationrequest_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ConsultationRequestUpdateView(BaseAdminUpdateView):
    model = ConsultationRequest
    fields = ['is_processed', 'direction', 'date', 'time', 'contact_phone', 'contact_email', 'additional_wishes']
    template_name = 'dashboards/crud/consultations/consultationrequest_form.html'
    success_url = reverse_lazy('dashboards:consultationrequest_list')
    success_message = "Заявка обновлена"

class ConsultationRequestDeleteView(BaseAdminDeleteView):
    model = ConsultationRequest
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:consultationrequest_list')
    success_message = "Заявка удалена"

# ---------------------- HeroSlide ----------------------
class HeroSlideListView(BaseAdminListView):
    model = HeroSlide
    template_name = 'dashboards/crud/consultations/heroslide_list.html'
    context_object_name = 'items'

class HeroSlideCreateView(BaseAdminCreateView):
    model = HeroSlide
    fields = ['title', 'subtitle', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/consultations/heroslide_form.html'
    success_url = reverse_lazy('dashboards:heroslide_list')
    success_message = "Слайд добавлен"

class HeroSlideUpdateView(BaseAdminUpdateView):
    model = HeroSlide
    fields = ['title', 'subtitle', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/consultations/heroslide_form.html'
    success_url = reverse_lazy('dashboards:heroslide_list')
    success_message = "Слайд обновлен"

class HeroSlideDeleteView(BaseAdminDeleteView):
    model = HeroSlide
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:heroslide_list')
    success_message = "Слайд удален"

# ---------------------- FAQ ----------------------
class FAQListView(BaseAdminListView):
    model = FAQ
    template_name = 'dashboards/crud/consultations/faq_list.html'
    context_object_name = 'items'

class FAQCreateView(BaseAdminCreateView):
    model = FAQ
    fields = ['question', 'answer', 'order', 'is_active']
    template_name = 'dashboards/crud/consultations/faq_form.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ добавлен"

class FAQUpdateView(BaseAdminUpdateView):
    model = FAQ
    fields = ['question', 'answer', 'order', 'is_active']
    template_name = 'dashboards/crud/consultations/faq_form.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ обновлен"

class FAQDeleteView(BaseAdminDeleteView):
    model = FAQ
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:faq_list')
    success_message = "FAQ удален"

# ---------------------- SuccessPageImage ----------------------
class SuccessPageImageListView(BaseAdminListView):
    model = SuccessPageImage
    template_name = 'dashboards/crud/consultations/successpageimage_list.html'
    context_object_name = 'items'

class SuccessPageImageCreateView(BaseAdminCreateView):
    model = SuccessPageImage
    fields = ['image', 'alt_text', 'is_active']
    template_name = 'dashboards/crud/consultations/successpageimage_form.html'
    success_url = reverse_lazy('dashboards:successpageimage_list')
    success_message = "Изображение добавлено"

class SuccessPageImageUpdateView(BaseAdminUpdateView):
    model = SuccessPageImage
    fields = ['image', 'alt_text', 'is_active']
    template_name = 'dashboards/crud/consultations/successpageimage_form.html'
    success_url = reverse_lazy('dashboards:successpageimage_list')
    success_message = "Изображение обновлено"

class SuccessPageImageDeleteView(BaseAdminDeleteView):
    model = SuccessPageImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:successpageimage_list')
    success_message = "Изображение удалено"