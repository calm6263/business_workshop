from django.urls import reverse_lazy

from partners.models import HomePageSlider, Partner, PartnershipApplication, LogoCarousel
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- HomePageSlider ----------------------
class HomePageSliderListView(BaseAdminListView):
    model = HomePageSlider
    template_name = 'dashboards/crud/partners/homeslider_list.html'
    context_object_name = 'items'

class HomePageSliderCreateView(BaseAdminCreateView):
    model = HomePageSlider
    fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/homeslider_form.html'
    success_url = reverse_lazy('dashboards:homeslider_list')
    success_message = "Слайд успешно добавлен"

class HomePageSliderUpdateView(BaseAdminUpdateView):
    model = HomePageSlider
    fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/homeslider_form.html'
    success_url = reverse_lazy('dashboards:homeslider_list')
    success_message = "Слайд успешно обновлен"

class HomePageSliderDeleteView(BaseAdminDeleteView):
    model = HomePageSlider
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:homeslider_list')
    success_message = "Слайд удален"

# ---------------------- Partner ----------------------
class PartnerListView(BaseAdminListView):
    model = Partner
    template_name = 'dashboards/crud/partners/partner_list.html'
    context_object_name = 'items'
    paginate_by = 20

class PartnerCreateView(BaseAdminCreateView):
    model = Partner
    fields = ['name', 'description', 'partner_type', 'logo', 'website',
              'show_in_carousel', 'show_in_grid', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/partner_form.html'
    success_url = reverse_lazy('dashboards:partner_list')
    success_message = "Партнер успешно добавлен"

class PartnerUpdateView(BaseAdminUpdateView):
    model = Partner
    fields = ['name', 'description', 'partner_type', 'logo', 'website',
              'show_in_carousel', 'show_in_grid', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/partner_form.html'
    success_url = reverse_lazy('dashboards:partner_list')
    success_message = "Партнер успешно обновлен"

class PartnerDeleteView(BaseAdminDeleteView):
    model = Partner
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:partner_list')
    success_message = "Партнер удален"

# ---------------------- PartnershipApplication ----------------------
class PartnershipApplicationListView(BaseAdminListView):
    model = PartnershipApplication
    template_name = 'dashboards/crud/partners/application_list.html'
    context_object_name = 'items'
    paginate_by = 20

class PartnershipApplicationUpdateView(BaseAdminUpdateView):
    model = PartnershipApplication
    fields = ['status', 'comments']
    template_name = 'dashboards/crud/partners/application_form.html'
    success_url = reverse_lazy('dashboards:application_list')
    success_message = "Статус заявки обновлен"

class PartnershipApplicationDeleteView(BaseAdminDeleteView):
    model = PartnershipApplication
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:application_list')
    success_message = "Заявка удалена"

# ---------------------- LogoCarousel ----------------------
class LogoCarouselListView(BaseAdminListView):
    model = LogoCarousel
    template_name = 'dashboards/crud/partners/logocarousel_list.html'
    context_object_name = 'items'

class LogoCarouselCreateView(BaseAdminCreateView):
    model = LogoCarousel
    fields = ['partner', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/logocarousel_form.html'
    success_url = reverse_lazy('dashboards:logocarousel_list')
    success_message = "Запись в карусели добавлена"

class LogoCarouselUpdateView(BaseAdminUpdateView):
    model = LogoCarousel
    fields = ['partner', 'order', 'is_active']
    template_name = 'dashboards/crud/partners/logocarousel_form.html'
    success_url = reverse_lazy('dashboards:logocarousel_list')
    success_message = "Запись в карусели обновлена"

class LogoCarouselDeleteView(BaseAdminDeleteView):
    model = LogoCarousel
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:logocarousel_list')
    success_message = "Запись удалена"