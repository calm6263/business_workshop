from django.urls import reverse_lazy
from django.http import Http404

from fta_journal.models import JournalIssue, SliderImage, SectionSettings, IssuePage
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- JournalIssue ----------------------
class JournalIssueListView(BaseAdminListView):
    model = JournalIssue
    template_name = 'dashboards/crud/fta_journal/journalissue_list.html'
    context_object_name = 'items'
    paginate_by = 20

class JournalIssueCreateView(BaseAdminCreateView):
    model = JournalIssue
    fields = [
        'title', 'description', 'cover_image', 'publication_date', 'pdf_file',
        'is_published', 'order', 'show_in_best', 'show_in_new',
        'best_order', 'new_order'
    ]
    template_name = 'dashboards/crud/fta_journal/journalissue_form.html'
    success_url = reverse_lazy('dashboards:journalissue_list')
    success_message = "Выпуск успешно создан"

class JournalIssueUpdateView(BaseAdminUpdateView):
    model = JournalIssue
    fields = [
        'title', 'description', 'cover_image', 'publication_date', 'pdf_file',
        'is_published', 'order', 'show_in_best', 'show_in_new',
        'best_order', 'new_order'
    ]
    template_name = 'dashboards/crud/fta_journal/journalissue_form.html'
    success_url = reverse_lazy('dashboards:journalissue_list')
    success_message = "Выпуск успешно обновлён"

class JournalIssueDeleteView(BaseAdminDeleteView):
    model = JournalIssue
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:journalissue_list')
    success_message = "Выпуск удалён"

# ---------------------- SliderImage ----------------------
class SliderImageListView(BaseAdminListView):
    model = SliderImage
    template_name = 'dashboards/crud/fta_journal/sliderimage_list.html'
    context_object_name = 'items'

class SliderImageCreateView(BaseAdminCreateView):
    model = SliderImage
    fields = ['title', 'image', 'description', 'link', 'order', 'is_active', 'carousel_type']
    template_name = 'dashboards/crud/fta_journal/sliderimage_form.html'
    success_url = reverse_lazy('dashboards:sliderimage_list')
    success_message = "Изображение слайдера добавлено"

class SliderImageUpdateView(BaseAdminUpdateView):
    model = SliderImage
    fields = ['title', 'image', 'description', 'link', 'order', 'is_active', 'carousel_type']
    template_name = 'dashboards/crud/fta_journal/sliderimage_form.html'
    success_url = reverse_lazy('dashboards:sliderimage_list')
    success_message = "Изображение слайдера обновлено"

class SliderImageDeleteView(BaseAdminDeleteView):
    model = SliderImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:sliderimage_list')
    success_message = "Изображение слайдера удалено"

# ---------------------- SectionSettings (singleton) ----------------------
class SectionSettingsListView(BaseAdminListView):
    model = SectionSettings
    template_name = 'dashboards/crud/fta_journal/sectionsettings_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return SectionSettings.objects.all()[:1]

class SectionSettingsCreateView(BaseAdminCreateView):
    model = SectionSettings
    fields = ['best_section_title', 'new_section_title', 'early_section_title']
    template_name = 'dashboards/crud/fta_journal/sectionsettings_form.html'
    success_url = reverse_lazy('dashboards:sectionsettings_list')
    success_message = "Настройки разделов созданы"

    def dispatch(self, request, *args, **kwargs):
        if SectionSettings.objects.exists():
            raise Http404("Настройки уже существуют. Вы можете только редактировать их.")
        return super().dispatch(request, *args, **kwargs)

class SectionSettingsUpdateView(BaseAdminUpdateView):
    model = SectionSettings
    fields = ['best_section_title', 'new_section_title', 'early_section_title']
    template_name = 'dashboards/crud/fta_journal/sectionsettings_form.html'
    success_url = reverse_lazy('dashboards:sectionsettings_list')
    success_message = "Настройки разделов обновлены"

class SectionSettingsDeleteView(BaseAdminDeleteView):
    model = SectionSettings
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:sectionsettings_list')
    success_message = "Настройки разделов удалены"

# ---------------------- IssuePage ----------------------
class IssuePageListView(BaseAdminListView):
    model = IssuePage
    template_name = 'dashboards/crud/fta_journal/issuepage_list.html'
    context_object_name = 'items'
    paginate_by = 30

    def get_queryset(self):
        qs = IssuePage.objects.all().select_related('issue')
        issue_id = self.request.GET.get('issue')
        if issue_id:
            qs = qs.filter(issue_id=issue_id)
        return qs

class IssuePageCreateView(BaseAdminCreateView):
    model = IssuePage
    fields = ['issue', 'image', 'page_number', 'order']
    template_name = 'dashboards/crud/fta_journal/issuepage_form.html'
    success_url = reverse_lazy('dashboards:issuepage_list')
    success_message = "Страница выпуска добавлена"

class IssuePageUpdateView(BaseAdminUpdateView):
    model = IssuePage
    fields = ['issue', 'image', 'page_number', 'order']
    template_name = 'dashboards/crud/fta_journal/issuepage_form.html'
    success_url = reverse_lazy('dashboards:issuepage_list')
    success_message = "Страница выпуска обновлена"

class IssuePageDeleteView(BaseAdminDeleteView):
    model = IssuePage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:issuepage_list')
    success_message = "Страница выпуска удалена"