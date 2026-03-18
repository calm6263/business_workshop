from django.urls import reverse_lazy

from schedule.models import (
    ScheduleProgram, CurriculumModule, CurriculumDocument,
    ProgramApplication, ScheduleSliderImage, CalendarSliderImage
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ScheduleProgram ----------------------
class ScheduleProgramListView(BaseAdminListView):
    model = ScheduleProgram
    template_name = 'dashboards/crud/schedule/scheduleprogram_list.html'
    context_object_name = 'items'
    paginate_by = 25

class ScheduleProgramCreateView(BaseAdminCreateView):
    model = ScheduleProgram
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/scheduleprogram_form.html'
    success_url = reverse_lazy('dashboards:scheduleprogram_list')
    success_message = "Программа успешно создана"

class ScheduleProgramUpdateView(BaseAdminUpdateView):
    model = ScheduleProgram
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/scheduleprogram_form.html'
    success_url = reverse_lazy('dashboards:scheduleprogram_list')
    success_message = "Программа успешно обновлена"

class ScheduleProgramDeleteView(BaseAdminDeleteView):
    model = ScheduleProgram
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:scheduleprogram_list')
    success_message = "Программа удалена"

# ---------------------- CurriculumModule ----------------------
class CurriculumModuleListView(BaseAdminListView):
    model = CurriculumModule
    template_name = 'dashboards/crud/schedule/curriculummodule_list.html'
    context_object_name = 'items'
    paginate_by = 25

class CurriculumModuleCreateView(BaseAdminCreateView):
    model = CurriculumModule
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/curriculummodule_form.html'
    success_url = reverse_lazy('dashboards:curriculummodule_list')
    success_message = "Модуль успешно создан"

class CurriculumModuleUpdateView(BaseAdminUpdateView):
    model = CurriculumModule
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/curriculummodule_form.html'
    success_url = reverse_lazy('dashboards:curriculummodule_list')
    success_message = "Модуль успешно обновлен"

class CurriculumModuleDeleteView(BaseAdminDeleteView):
    model = CurriculumModule
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:curriculummodule_list')
    success_message = "Модуль удален"

# ---------------------- CurriculumDocument ----------------------
class CurriculumDocumentListView(BaseAdminListView):
    model = CurriculumDocument
    template_name = 'dashboards/crud/schedule/curriculumdocument_list.html'
    context_object_name = 'items'
    paginate_by = 25

class CurriculumDocumentCreateView(BaseAdminCreateView):
    model = CurriculumDocument
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/curriculumdocument_form.html'
    success_url = reverse_lazy('dashboards:curriculumdocument_list')
    success_message = "Документ успешно создан"

class CurriculumDocumentUpdateView(BaseAdminUpdateView):
    model = CurriculumDocument
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/curriculumdocument_form.html'
    success_url = reverse_lazy('dashboards:curriculumdocument_list')
    success_message = "Документ успешно обновлен"

class CurriculumDocumentDeleteView(BaseAdminDeleteView):
    model = CurriculumDocument
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:curriculumdocument_list')
    success_message = "Документ удален"

# ---------------------- ProgramApplication ----------------------
class ProgramApplicationListView(BaseAdminListView):
    model = ProgramApplication
    template_name = 'dashboards/crud/schedule/programapplication_list.html'
    context_object_name = 'items'
    paginate_by = 25

class ProgramApplicationCreateView(BaseAdminCreateView):
    model = ProgramApplication
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/programapplication_form.html'
    success_url = reverse_lazy('dashboards:programapplication_list')
    success_message = "Заявка успешно создана"

class ProgramApplicationUpdateView(BaseAdminUpdateView):
    model = ProgramApplication
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/programapplication_form.html'
    success_url = reverse_lazy('dashboards:programapplication_list')
    success_message = "Заявка успешно обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'application_number' in form.fields:
            form.fields['application_number'].disabled = True
        return form

class ProgramApplicationDeleteView(BaseAdminDeleteView):
    model = ProgramApplication
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:programapplication_list')
    success_message = "Заявка удалена"

# ---------------------- ScheduleSliderImage ----------------------
class ScheduleSliderImageListView(BaseAdminListView):
    model = ScheduleSliderImage
    template_name = 'dashboards/crud/schedule/schedulesliderimage_list.html'
    context_object_name = 'items'
    paginate_by = 25

class ScheduleSliderImageCreateView(BaseAdminCreateView):
    model = ScheduleSliderImage
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/schedulesliderimage_form.html'
    success_url = reverse_lazy('dashboards:schedulesliderimage_list')
    success_message = "Изображение слайдера успешно создано"

class ScheduleSliderImageUpdateView(BaseAdminUpdateView):
    model = ScheduleSliderImage
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/schedulesliderimage_form.html'
    success_url = reverse_lazy('dashboards:schedulesliderimage_list')
    success_message = "Изображение слайдера успешно обновлено"

class ScheduleSliderImageDeleteView(BaseAdminDeleteView):
    model = ScheduleSliderImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:schedulesliderimage_list')
    success_message = "Изображение слайдера удалено"

# ---------------------- CalendarSliderImage ----------------------
class CalendarSliderImageListView(BaseAdminListView):
    model = CalendarSliderImage
    template_name = 'dashboards/crud/schedule/calendarsliderimage_list.html'
    context_object_name = 'items'
    paginate_by = 25

class CalendarSliderImageCreateView(BaseAdminCreateView):
    model = CalendarSliderImage
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/calendarsliderimage_form.html'
    success_url = reverse_lazy('dashboards:calendarsliderimage_list')
    success_message = "Изображение слайдера календаря успешно создано"

class CalendarSliderImageUpdateView(BaseAdminUpdateView):
    model = CalendarSliderImage
    fields = '__all__'
    template_name = 'dashboards/crud/schedule/calendarsliderimage_form.html'
    success_url = reverse_lazy('dashboards:calendarsliderimage_list')
    success_message = "Изображение слайдера календаря успешно обновлено"

class CalendarSliderImageDeleteView(BaseAdminDeleteView):
    model = CalendarSliderImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:calendarsliderimage_list')
    success_message = "Изображение слайдера календаря удалено"