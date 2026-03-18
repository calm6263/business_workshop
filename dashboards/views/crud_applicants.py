from django.urls import reverse_lazy
from django.http import Http404

from applicants.models import (
    ApplicantsPage, ApplicationMethod, EnrollmentStage,
    ApplicantDocument, ApplicantApplication
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ApplicantsPage (Singleton) ----------------------
class ApplicantsPageListView(BaseAdminListView):
    model = ApplicantsPage
    template_name = 'dashboards/crud/applicants/applicantspage_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return ApplicantsPage.objects.all()[:1]

class ApplicantsPageCreateView(BaseAdminCreateView):
    model = ApplicantsPage
    fields = ['title', 'background_image', 'rocket_image',
              'conditions_file', 'enrollment_conditions_file',
              'programs_list_file', 'benefits_file',
              'contract_sample_file', 'useful_links_file',
              'methods_review_text', 'methods_login_text', 'is_active']
    template_name = 'dashboards/crud/applicants/applicantspage_form.html'
    success_url = reverse_lazy('dashboards:applicantspage_list')
    success_message = "Страница успешно создана"

    def dispatch(self, request, *args, **kwargs):
        if ApplicantsPage.objects.exists():
            raise Http404("Страница уже существует. Вы можете только редактировать её.")
        return super().dispatch(request, *args, **kwargs)

class ApplicantsPageUpdateView(BaseAdminUpdateView):
    model = ApplicantsPage
    fields = ['title', 'background_image', 'rocket_image',
              'conditions_file', 'enrollment_conditions_file',
              'programs_list_file', 'benefits_file',
              'contract_sample_file', 'useful_links_file',
              'methods_review_text', 'methods_login_text', 'is_active']
    template_name = 'dashboards/crud/applicants/applicantspage_form.html'
    success_url = reverse_lazy('dashboards:applicantspage_list')
    success_message = "Страница успешно обновлена"

class ApplicantsPageDeleteView(BaseAdminDeleteView):
    model = ApplicantsPage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:applicantspage_list')
    success_message = "Страница удалена"

# ---------------------- ApplicationMethod ----------------------
class ApplicationMethodListView(BaseAdminListView):
    model = ApplicationMethod
    template_name = 'dashboards/crud/applicants/applicationmethod_list.html'
    context_object_name = 'items'

class ApplicationMethodCreateView(BaseAdminCreateView):
    model = ApplicationMethod
    fields = ['title', 'icon_svg', 'question_svg', 'order', 'is_active']
    template_name = 'dashboards/crud/applicants/applicationmethod_form.html'
    success_url = reverse_lazy('dashboards:applicationmethod_list')
    success_message = "Способ подачи добавлен"

class ApplicationMethodUpdateView(BaseAdminUpdateView):
    model = ApplicationMethod
    fields = ['title', 'icon_svg', 'question_svg', 'order', 'is_active']
    template_name = 'dashboards/crud/applicants/applicationmethod_form.html'
    success_url = reverse_lazy('dashboards:applicationmethod_list')
    success_message = "Способ подачи обновлен"

class ApplicationMethodDeleteView(BaseAdminDeleteView):
    model = ApplicationMethod
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:applicationmethod_list')
    success_message = "Способ подачи удален"

# ---------------------- EnrollmentStage ----------------------
class EnrollmentStageListView(BaseAdminListView):
    model = EnrollmentStage
    template_name = 'dashboards/crud/applicants/enrollmentstage_list.html'
    context_object_name = 'items'

class EnrollmentStageCreateView(BaseAdminCreateView):
    model = EnrollmentStage
    fields = ['name', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/applicants/enrollmentstage_form.html'
    success_url = reverse_lazy('dashboards:enrollmentstage_list')
    success_message = "Этап зачисления добавлен"

class EnrollmentStageUpdateView(BaseAdminUpdateView):
    model = EnrollmentStage
    fields = ['name', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/applicants/enrollmentstage_form.html'
    success_url = reverse_lazy('dashboards:enrollmentstage_list')
    success_message = "Этап зачисления обновлен"

class EnrollmentStageDeleteView(BaseAdminDeleteView):
    model = EnrollmentStage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:enrollmentstage_list')
    success_message = "Этап зачисления удален"

# ---------------------- ApplicantDocument ----------------------
class ApplicantDocumentListView(BaseAdminListView):
    model = ApplicantDocument
    template_name = 'dashboards/crud/applicants/applicantdocument_list.html'
    context_object_name = 'items'

class ApplicantDocumentCreateView(BaseAdminCreateView):
    model = ApplicantDocument
    fields = ['name', 'file', 'is_active']
    template_name = 'dashboards/crud/applicants/applicantdocument_form.html'
    success_url = reverse_lazy('dashboards:applicantdocument_list')
    success_message = "Документ добавлен"

class ApplicantDocumentUpdateView(BaseAdminUpdateView):
    model = ApplicantDocument
    fields = ['name', 'file', 'is_active']
    template_name = 'dashboards/crud/applicants/applicantdocument_form.html'
    success_url = reverse_lazy('dashboards:applicantdocument_list')
    success_message = "Документ обновлен"

class ApplicantDocumentDeleteView(BaseAdminDeleteView):
    model = ApplicantDocument
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:applicantdocument_list')
    success_message = "Документ удален"

# ---------------------- ApplicantApplication ----------------------
class ApplicantApplicationListView(BaseAdminListView):
    model = ApplicantApplication
    template_name = 'dashboards/crud/applicants/applicantapplication_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ApplicantApplicationCreateView(BaseAdminCreateView):
    model = ApplicantApplication
    fields = ['contact_person', 'phone', 'email', 'additional_notes', 'status']
    template_name = 'dashboards/crud/applicants/applicantapplication_form.html'
    success_url = reverse_lazy('dashboards:applicantapplication_list')
    success_message = "Заявка добавлена"

class ApplicantApplicationUpdateView(BaseAdminUpdateView):
    model = ApplicantApplication
    fields = ['contact_person', 'phone', 'email', 'additional_notes', 'status']
    template_name = 'dashboards/crud/applicants/applicantapplication_form.html'
    success_url = reverse_lazy('dashboards:applicantapplication_list')
    success_message = "Заявка обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'application_number' in form.fields:
            form.fields['application_number'].disabled = True
        return form

class ApplicantApplicationDeleteView(BaseAdminDeleteView):
    model = ApplicantApplication
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:applicantapplication_list')
    success_message = "Заявка удалена"