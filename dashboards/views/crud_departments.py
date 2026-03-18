from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404

from departments.models import Department, HeroImage
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- Department ----------------------
class DepartmentListView(BaseAdminListView):
    model = Department
    template_name = 'dashboards/crud/departments/department_list.html'
    context_object_name = 'items'

class DepartmentCreateView(BaseAdminCreateView):
    model = Department
    fields = ['name', 'program_type', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/departments/department_form.html'
    success_url = reverse_lazy('dashboards:department_list')
    success_message = "Отделение успешно добавлено"

class DepartmentUpdateView(BaseAdminUpdateView):
    model = Department
    fields = ['name', 'program_type', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/departments/department_form.html'
    success_url = reverse_lazy('dashboards:department_list')
    success_message = "Отделение успешно обновлено"

class DepartmentDeleteView(BaseAdminDeleteView):
    model = Department
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:department_list')
    success_message = "Отделение удалено"

# ---------------------- HeroImage (singleton per page) ----------------------
class HeroImageListView(BaseAdminListView):
    model = HeroImage
    template_name = 'dashboards/crud/departments/heroimage_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return HeroImage.objects.all()

class HeroImageCreateView(BaseAdminCreateView):
    model = HeroImage
    fields = ['page', 'title', 'subtitle', 'description', 'image', 'link_text', 'link', 'is_active', 'order']
    template_name = 'dashboards/crud/departments/heroimage_form.html'
    success_url = reverse_lazy('dashboards:heroimage_list')
    success_message = "Изображение героя успешно создано"

    def dispatch(self, request, *args, **kwargs):
        page = request.POST.get('page') or request.GET.get('page')
        if page and HeroImage.objects.filter(page=page).exists():
            messages.error(request, f"Запись для страницы '{page}' уже существует. Вы можете только редактировать её.")
            return redirect('dashboards:heroimage_list')
        return super().dispatch(request, *args, **kwargs)

class HeroImageUpdateView(BaseAdminUpdateView):
    model = HeroImage
    fields = ['page', 'title', 'subtitle', 'description', 'image', 'link_text', 'link', 'is_active', 'order']
    template_name = 'dashboards/crud/departments/heroimage_form.html'
    success_url = reverse_lazy('dashboards:heroimage_list')
    success_message = "Изображение героя успешно обновлено"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['page'].disabled = True
        return form

class HeroImageDeleteView(BaseAdminDeleteView):
    model = HeroImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:heroimage_list')
    success_message = "Изображение героя удалено"