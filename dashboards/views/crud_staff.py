from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404

from staff.models import TeamMember, TeacherProgram, PageHero
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- TeamMember ----------------------
class TeamMemberListView(BaseAdminListView):
    model = TeamMember
    template_name = 'dashboards/crud/staff/teammember_list.html'
    context_object_name = 'items'
    paginate_by = 20

class TeamMemberCreateView(BaseAdminCreateView):
    model = TeamMember
    fields = [
        'name', 'image', 'position', 'description', 'email', 'phone',
        'qualifications', 'experience', 'member_type', 'departments',
        'order', 'is_active'
    ]
    template_name = 'dashboards/crud/staff/teammember_form.html'
    success_url = reverse_lazy('dashboards:teammember_list')
    success_message = "Член команды успешно добавлен"

class TeamMemberUpdateView(BaseAdminUpdateView):
    model = TeamMember
    fields = [
        'name', 'image', 'position', 'description', 'email', 'phone',
        'qualifications', 'experience', 'member_type', 'departments',
        'order', 'is_active'
    ]
    template_name = 'dashboards/crud/staff/teammember_form.html'
    success_url = reverse_lazy('dashboards:teammember_list')
    success_message = "Член команды успешно обновлён"

class TeamMemberDeleteView(BaseAdminDeleteView):
    model = TeamMember
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:teammember_list')
    success_message = "Член команды удалён"

# ---------------------- TeacherProgram ----------------------
class TeacherProgramListView(BaseAdminListView):
    model = TeacherProgram
    template_name = 'dashboards/crud/staff/teacherprogram_list.html'
    context_object_name = 'items'
    paginate_by = 20

class TeacherProgramCreateView(BaseAdminCreateView):
    model = TeacherProgram
    fields = ['teacher', 'program', 'role', 'order', 'is_active']
    template_name = 'dashboards/crud/staff/teacherprogram_form.html'
    success_url = reverse_lazy('dashboards:teacherprogram_list')
    success_message = "Программа преподавателя добавлена"

class TeacherProgramUpdateView(BaseAdminUpdateView):
    model = TeacherProgram
    fields = ['teacher', 'program', 'role', 'order', 'is_active']
    template_name = 'dashboards/crud/staff/teacherprogram_form.html'
    success_url = reverse_lazy('dashboards:teacherprogram_list')
    success_message = "Программа преподавателя обновлена"

class TeacherProgramDeleteView(BaseAdminDeleteView):
    model = TeacherProgram
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:teacherprogram_list')
    success_message = "Программа преподавателя удалена"

# ---------------------- PageHero (singleton per page) ----------------------
class PageHeroListView(BaseAdminListView):
    model = PageHero
    template_name = 'dashboards/crud/staff/pagehero_list.html'
    context_object_name = 'items'

class PageHeroCreateView(BaseAdminCreateView):
    model = PageHero
    fields = ['page', 'title', 'subtitle', 'image', 'is_active']
    template_name = 'dashboards/crud/staff/pagehero_form.html'
    success_url = reverse_lazy('dashboards:pagehero_list')
    success_message = "Hero-секция создана"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            page = request.POST.get('page')
            if page and PageHero.objects.filter(page=page).exists():
                messages.error(request, "Hero-секция для этой страницы уже существует. Вы можете отредактировать её.")
                return redirect('dashboards:pagehero_list')
        return super().dispatch(request, *args, **kwargs)

class PageHeroUpdateView(BaseAdminUpdateView):
    model = PageHero
    fields = ['title', 'subtitle', 'image', 'is_active']
    template_name = 'dashboards/crud/staff/pagehero_form.html'
    success_url = reverse_lazy('dashboards:pagehero_list')
    success_message = "Hero-секция обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['page'].disabled = True
        return form

class PageHeroDeleteView(BaseAdminDeleteView):
    model = PageHero
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:pagehero_list')
    success_message = "Hero-секция удалена"