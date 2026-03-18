from django.urls import reverse_lazy
from django.http import Http404

from contacts.models import (
    ContactSection, OrganizationInfo, SocialMedia,
    ContactPageSettings, ContactHero
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ContactSection ----------------------
class ContactSectionListView(BaseAdminListView):
    model = ContactSection
    template_name = 'dashboards/crud/contacts/contactsection_list.html'
    context_object_name = 'items'

class ContactSectionCreateView(BaseAdminCreateView):
    model = ContactSection
    fields = ['title', 'section_type', 'department_name', 'description',
              'phone', 'email', 'additional_phones', 'additional_emails',
              'address', 'work_hours', 'order', 'is_active']
    template_name = 'dashboards/crud/contacts/contactsection_form.html'
    success_url = reverse_lazy('dashboards:contactsection_list')
    success_message = "Раздел контактов успешно добавлен"

class ContactSectionUpdateView(BaseAdminUpdateView):
    model = ContactSection
    fields = ['title', 'section_type', 'department_name', 'description',
              'phone', 'email', 'additional_phones', 'additional_emails',
              'address', 'work_hours', 'order', 'is_active']
    template_name = 'dashboards/crud/contacts/contactsection_form.html'
    success_url = reverse_lazy('dashboards:contactsection_list')
    success_message = "Раздел контактов успешно обновлён"

class ContactSectionDeleteView(BaseAdminDeleteView):
    model = ContactSection
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:contactsection_list')
    success_message = "Раздел контактов удалён"

# ---------------------- OrganizationInfo (Singleton) ----------------------
class OrganizationInfoListView(BaseAdminListView):
    model = OrganizationInfo
    template_name = 'dashboards/crud/contacts/organizationinfo_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return OrganizationInfo.objects.all()[:1]

class OrganizationInfoCreateView(BaseAdminCreateView):
    model = OrganizationInfo
    fields = ['name', 'full_name', 'general_phone', 'general_email',
              'additional_phones', 'address', 'description', 'logo']
    template_name = 'dashboards/crud/contacts/organizationinfo_form.html'
    success_url = reverse_lazy('dashboards:organizationinfo_list')
    success_message = "Информация об организации создана"

    def dispatch(self, request, *args, **kwargs):
        if OrganizationInfo.objects.exists():
            raise Http404("Запись уже существует. Вы можете только редактировать её.")
        return super().dispatch(request, *args, **kwargs)

class OrganizationInfoUpdateView(BaseAdminUpdateView):
    model = OrganizationInfo
    fields = ['name', 'full_name', 'general_phone', 'general_email',
              'additional_phones', 'address', 'description', 'logo']
    template_name = 'dashboards/crud/contacts/organizationinfo_form.html'
    success_url = reverse_lazy('dashboards:organizationinfo_list')
    success_message = "Информация об организации обновлена"

class OrganizationInfoDeleteView(BaseAdminDeleteView):
    model = OrganizationInfo
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:organizationinfo_list')
    success_message = "Информация об организации удалена"

# ---------------------- SocialMedia ----------------------
class SocialMediaListView(BaseAdminListView):
    model = SocialMedia
    template_name = 'dashboards/crud/contacts/socialmedia_list.html'
    context_object_name = 'items'

class SocialMediaCreateView(BaseAdminCreateView):
    model = SocialMedia
    fields = ['name', 'url', 'icon_class', 'order', 'is_active']
    template_name = 'dashboards/crud/contacts/socialmedia_form.html'
    success_url = reverse_lazy('dashboards:socialmedia_list')
    success_message = "Социальная сеть добавлена"

class SocialMediaUpdateView(BaseAdminUpdateView):
    model = SocialMedia
    fields = ['name', 'url', 'icon_class', 'order', 'is_active']
    template_name = 'dashboards/crud/contacts/socialmedia_form.html'
    success_url = reverse_lazy('dashboards:socialmedia_list')
    success_message = "Социальная сеть обновлена"

class SocialMediaDeleteView(BaseAdminDeleteView):
    model = SocialMedia
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:socialmedia_list')
    success_message = "Социальная сеть удалена"

# ---------------------- ContactPageSettings (Singleton) ----------------------
class ContactPageSettingsListView(BaseAdminListView):
    model = ContactPageSettings
    template_name = 'dashboards/crud/contacts/contactpagesettings_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return ContactPageSettings.objects.all()[:1]

class ContactPageSettingsCreateView(BaseAdminCreateView):
    model = ContactPageSettings
    fields = ['meta_title', 'meta_description', 'show_breadcrumbs', 'show_organization_info']
    template_name = 'dashboards/crud/contacts/contactpagesettings_form.html'
    success_url = reverse_lazy('dashboards:contactpagesettings_list')
    success_message = "Настройки страницы созданы"

    def dispatch(self, request, *args, **kwargs):
        if ContactPageSettings.objects.exists():
            raise Http404("Настройки уже существуют. Вы можете только редактировать их.")
        return super().dispatch(request, *args, **kwargs)

class ContactPageSettingsUpdateView(BaseAdminUpdateView):
    model = ContactPageSettings
    fields = ['meta_title', 'meta_description', 'show_breadcrumbs', 'show_organization_info']
    template_name = 'dashboards/crud/contacts/contactpagesettings_form.html'
    success_url = reverse_lazy('dashboards:contactpagesettings_list')
    success_message = "Настройки страницы обновлены"

class ContactPageSettingsDeleteView(BaseAdminDeleteView):
    model = ContactPageSettings
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:contactpagesettings_list')
    success_message = "Настройки страницы удалены"

# ---------------------- ContactHero ----------------------
class ContactHeroListView(BaseAdminListView):
    model = ContactHero
    template_name = 'dashboards/crud/contacts/contacthero_list.html'
    context_object_name = 'items'

class ContactHeroCreateView(BaseAdminCreateView):
    model = ContactHero
    fields = ['title', 'subtitle', 'description', 'image', 'show_breadcrumb', 'is_active']
    template_name = 'dashboards/crud/contacts/contacthero_form.html'
    success_url = reverse_lazy('dashboards:contacthero_list')
    success_message = "Hero-раздел добавлен"

class ContactHeroUpdateView(BaseAdminUpdateView):
    model = ContactHero
    fields = ['title', 'subtitle', 'description', 'image', 'show_breadcrumb', 'is_active']
    template_name = 'dashboards/crud/contacts/contacthero_form.html'
    success_url = reverse_lazy('dashboards:contacthero_list')
    success_message = "Hero-раздел обновлён"

class ContactHeroDeleteView(BaseAdminDeleteView):
    model = ContactHero
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:contacthero_list')
    success_message = "Hero-раздел удалён"