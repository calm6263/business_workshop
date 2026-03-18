# dashboards/views/crud_main.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from main.models import Slide, License
from .mixins import AdminRequiredMixin, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView, BaseAdminListView

# ---------------------- Slide CRUD ----------------------
class SlideListView(BaseAdminListView):
    model = Slide
    template_name = 'dashboards/crud/main/slide_list.html'
    paginate_by = 20

class SlideCreateView(BaseAdminCreateView):
    model = Slide
    fields = ['title', 'slide_type', 'image', 'video', 'caption', 'is_active', 'order']
    template_name = 'dashboards/crud/main/slide_form.html'
    success_url = reverse_lazy('dashboards:slide_list')
    success_message = "Слайд успешно создан"

class SlideUpdateView(BaseAdminUpdateView):
    model = Slide
    fields = ['title', 'slide_type', 'image', 'video', 'caption', 'is_active', 'order']
    template_name = 'dashboards/crud/main/slide_form.html'
    success_url = reverse_lazy('dashboards:slide_list')
    success_message = "Слайд успешно обновлен"

class SlideDeleteView(BaseAdminDeleteView):
    model = Slide
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:slide_list')
    success_message = "Слайд удален"

# ---------------------- License CRUD ----------------------
class LicenseListView(BaseAdminListView):
    model = License
    template_name = 'dashboards/crud/main/license_list.html'

class LicenseCreateView(BaseAdminCreateView):
    model = License
    fields = ['title', 'file', 'order', 'is_active']
    template_name = 'dashboards/crud/main/license_form.html'
    success_url = reverse_lazy('dashboards:license_list')
    success_message = "Лицензия успешно создана"

class LicenseUpdateView(BaseAdminUpdateView):
    model = License
    fields = ['title', 'file', 'order', 'is_active']
    template_name = 'dashboards/crud/main/license_form.html'
    success_url = reverse_lazy('dashboards:license_list')
    success_message = "Лицензия успешно обновлена"

class LicenseDeleteView(BaseAdminDeleteView):
    model = License
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:license_list')
    success_message = "Лицензия удалена"