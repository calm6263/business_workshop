from django.urls import reverse_lazy

from research.models import (
    ResearchCategory, Research, ResearchTag, ResearchHero,
    Conference, ConferenceRegistration,
    YouthCouncilDepartment, YouthCouncilMember
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ResearchCategory ----------------------
class ResearchCategoryListView(BaseAdminListView):
    model = ResearchCategory
    template_name = 'dashboards/crud/research/researchcategory_list.html'
    context_object_name = 'items'

class ResearchCategoryCreateView(BaseAdminCreateView):
    model = ResearchCategory
    fields = ['name', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/research/researchcategory_form.html'
    success_url = reverse_lazy('dashboards:researchcategory_list')
    success_message = "Категория успешно создана"

class ResearchCategoryUpdateView(BaseAdminUpdateView):
    model = ResearchCategory
    fields = ['name', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/research/researchcategory_form.html'
    success_url = reverse_lazy('dashboards:researchcategory_list')
    success_message = "Категория успешно обновлена"

class ResearchCategoryDeleteView(BaseAdminDeleteView):
    model = ResearchCategory
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:researchcategory_list')
    success_message = "Категория удалена"

# ---------------------- Research ----------------------
class ResearchListView(BaseAdminListView):
    model = Research
    template_name = 'dashboards/crud/research/research_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ResearchCreateView(BaseAdminCreateView):
    model = Research
    fields = [
        'title', 'research_type', 'category', 'description', 'short_description',
        'image', 'publication_date', 'author', 'file', 'is_featured', 'is_active'
    ]
    template_name = 'dashboards/crud/research/research_form.html'
    success_url = reverse_lazy('dashboards:research_list')
    success_message = "Исследование успешно добавлено"

class ResearchUpdateView(BaseAdminUpdateView):
    model = Research
    fields = [
        'title', 'research_type', 'category', 'description', 'short_description',
        'image', 'publication_date', 'author', 'file', 'is_featured', 'is_active'
    ]
    template_name = 'dashboards/crud/research/research_form.html'
    success_url = reverse_lazy('dashboards:research_list')
    success_message = "Исследование успешно обновлено"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'views_count' in form.fields:
            form.fields['views_count'].disabled = True
        return form

class ResearchDeleteView(BaseAdminDeleteView):
    model = Research
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:research_list')
    success_message = "Исследование удалено"

# ---------------------- ResearchTag ----------------------
class ResearchTagListView(BaseAdminListView):
    model = ResearchTag
    template_name = 'dashboards/crud/research/researchtag_list.html'
    context_object_name = 'items'

class ResearchTagCreateView(BaseAdminCreateView):
    model = ResearchTag
    fields = ['name', 'research']
    template_name = 'dashboards/crud/research/researchtag_form.html'
    success_url = reverse_lazy('dashboards:researchtag_list')
    success_message = "Тег успешно создан"

class ResearchTagUpdateView(BaseAdminUpdateView):
    model = ResearchTag
    fields = ['name', 'research']
    template_name = 'dashboards/crud/research/researchtag_form.html'
    success_url = reverse_lazy('dashboards:researchtag_list')
    success_message = "Тег успешно обновлен"

class ResearchTagDeleteView(BaseAdminDeleteView):
    model = ResearchTag
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:researchtag_list')
    success_message = "Тег удален"

# ---------------------- ResearchHero ----------------------
class ResearchHeroListView(BaseAdminListView):
    model = ResearchHero
    template_name = 'dashboards/crud/research/researchhero_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return ResearchHero.objects.all()

class ResearchHeroCreateView(BaseAdminCreateView):
    model = ResearchHero
    fields = ['title', 'background_image', 'brochure', 'is_active']
    template_name = 'dashboards/crud/research/researchhero_form.html'
    success_url = reverse_lazy('dashboards:researchhero_list')
    success_message = "Hero-раздел успешно создан"

class ResearchHeroUpdateView(BaseAdminUpdateView):
    model = ResearchHero
    fields = ['title', 'background_image', 'brochure', 'is_active']
    template_name = 'dashboards/crud/research/researchhero_form.html'
    success_url = reverse_lazy('dashboards:researchhero_list')
    success_message = "Hero-раздел успешно обновлен"

class ResearchHeroDeleteView(BaseAdminDeleteView):
    model = ResearchHero
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:researchhero_list')
    success_message = "Hero-раздел удален"

# ---------------------- Conference ----------------------
class ConferenceListView(BaseAdminListView):
    model = Conference
    template_name = 'dashboards/crud/research/conference_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ConferenceCreateView(BaseAdminCreateView):
    model = Conference
    fields = [
        'title', 'conference_type', 'description', 'short_description',
        'image', 'start_date', 'end_date', 'location', 'registration_link',
        'is_active', 'contact_person', 'contact_phone', 'contact_email',
        'organizers', 'video', 'video_title', 'file', 'entrance_fee'
    ]
    template_name = 'dashboards/crud/research/conference_form.html'
    success_url = reverse_lazy('dashboards:conference_list')
    success_message = "Конференция успешно создана"

class ConferenceUpdateView(BaseAdminUpdateView):
    model = Conference
    fields = [
        'title', 'conference_type', 'description', 'short_description',
        'image', 'start_date', 'end_date', 'location', 'registration_link',
        'is_active', 'contact_person', 'contact_phone', 'contact_email',
        'organizers', 'video', 'video_title', 'file', 'entrance_fee'
    ]
    template_name = 'dashboards/crud/research/conference_form.html'
    success_url = reverse_lazy('dashboards:conference_list')
    success_message = "Конференция успешно обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'views_count' in form.fields:
            form.fields['views_count'].disabled = True
        return form

class ConferenceDeleteView(BaseAdminDeleteView):
    model = Conference
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:conference_list')
    success_message = "Конференция удалена"

# ---------------------- ConferenceRegistration ----------------------
class ConferenceRegistrationListView(BaseAdminListView):
    model = ConferenceRegistration
    template_name = 'dashboards/crud/research/conferenceregistration_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ConferenceRegistrationCreateView(BaseAdminCreateView):
    model = ConferenceRegistration
    fields = ['conference', 'full_name', 'phone', 'email', 'agreement']
    template_name = 'dashboards/crud/research/conferenceregistration_form.html'
    success_url = reverse_lazy('dashboards:conferenceregistration_list')
    success_message = "Регистрация успешно добавлена"

class ConferenceRegistrationUpdateView(BaseAdminUpdateView):
    model = ConferenceRegistration
    fields = ['conference', 'full_name', 'phone', 'email', 'agreement']
    template_name = 'dashboards/crud/research/conferenceregistration_form.html'
    success_url = reverse_lazy('dashboards:conferenceregistration_list')
    success_message = "Регистрация успешно обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'registration_number' in form.fields:
            form.fields['registration_number'].disabled = True
        return form

class ConferenceRegistrationDeleteView(BaseAdminDeleteView):
    model = ConferenceRegistration
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:conferenceregistration_list')
    success_message = "Регистрация удалена"

# ---------------------- YouthCouncilDepartment ----------------------
class YouthCouncilDepartmentListView(BaseAdminListView):
    model = YouthCouncilDepartment
    template_name = 'dashboards/crud/research/youthcouncildepartment_list.html'
    context_object_name = 'items'

class YouthCouncilDepartmentCreateView(BaseAdminCreateView):
    model = YouthCouncilDepartment
    fields = ['name', 'order', 'is_active']
    template_name = 'dashboards/crud/research/youthcouncildepartment_form.html'
    success_url = reverse_lazy('dashboards:youthcouncildepartment_list')
    success_message = "Отделение успешно создано"

class YouthCouncilDepartmentUpdateView(BaseAdminUpdateView):
    model = YouthCouncilDepartment
    fields = ['name', 'order', 'is_active']
    template_name = 'dashboards/crud/research/youthcouncildepartment_form.html'
    success_url = reverse_lazy('dashboards:youthcouncildepartment_list')
    success_message = "Отделение успешно обновлено"

class YouthCouncilDepartmentDeleteView(BaseAdminDeleteView):
    model = YouthCouncilDepartment
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:youthcouncildepartment_list')
    success_message = "Отделение удалено"

# ---------------------- YouthCouncilMember ----------------------
class YouthCouncilMemberListView(BaseAdminListView):
    model = YouthCouncilMember
    template_name = 'dashboards/crud/research/youthcouncilmember_list.html'
    context_object_name = 'items'

class YouthCouncilMemberCreateView(BaseAdminCreateView):
    model = YouthCouncilMember
    fields = [
        'name', 'image', 'position', 'description', 'email', 'phone',
        'departments', 'order', 'is_active'
    ]
    template_name = 'dashboards/crud/research/youthcouncilmember_form.html'
    success_url = reverse_lazy('dashboards:youthcouncilmember_list')
    success_message = "Член совета успешно добавлен"

class YouthCouncilMemberUpdateView(BaseAdminUpdateView):
    model = YouthCouncilMember
    fields = [
        'name', 'image', 'position', 'description', 'email', 'phone',
        'departments', 'order', 'is_active'
    ]
    template_name = 'dashboards/crud/research/youthcouncilmember_form.html'
    success_url = reverse_lazy('dashboards:youthcouncilmember_list')
    success_message = "Член совета успешно обновлен"

class YouthCouncilMemberDeleteView(BaseAdminDeleteView):
    model = YouthCouncilMember
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:youthcouncilmember_list')
    success_message = "Член совета удален"