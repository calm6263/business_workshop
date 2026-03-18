from django.urls import reverse_lazy

from projects.models import (
    ProjectCategory, Project, ProjectMember, ProjectPartner,
    ProjectSlide, ContactRequest, ProjectProposal, ProjectGallery,
    ProjectJoinRequest
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView

# ---------------------- ProjectCategory ----------------------
class ProjectCategoryListView(BaseAdminListView):
    model = ProjectCategory
    template_name = 'dashboards/crud/projects/projectcategory_list.html'
    context_object_name = 'items'

class ProjectCategoryCreateView(BaseAdminCreateView):
    model = ProjectCategory
    fields = ['name', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectcategory_form.html'
    success_url = reverse_lazy('dashboards:projectcategory_list')
    success_message = "Категория успешно создана"

class ProjectCategoryUpdateView(BaseAdminUpdateView):
    model = ProjectCategory
    fields = ['name', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectcategory_form.html'
    success_url = reverse_lazy('dashboards:projectcategory_list')
    success_message = "Категория успешно обновлена"

class ProjectCategoryDeleteView(BaseAdminDeleteView):
    model = ProjectCategory
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectcategory_list')
    success_message = "Категория удалена"

# ---------------------- Project ----------------------
class ProjectListView(BaseAdminListView):
    model = Project
    template_name = 'dashboards/crud/projects/project_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ProjectCreateView(BaseAdminCreateView):
    model = Project
    fields = [
        'title', 'project_type', 'category', 'description', 'short_description',
        'sidebar_title', 'image', 'description_image', 'presentation_file',
        'start_date', 'end_date', 'status', 'budget', 'participants_count',
        'results', 'is_featured', 'is_active', 'order'
    ]
    template_name = 'dashboards/crud/projects/project_form.html'
    success_url = reverse_lazy('dashboards:project_list')
    success_message = "Проект успешно создан"

class ProjectUpdateView(BaseAdminUpdateView):
    model = Project
    fields = [
        'title', 'project_type', 'category', 'description', 'short_description',
        'sidebar_title', 'image', 'description_image', 'presentation_file',
        'start_date', 'end_date', 'status', 'budget', 'participants_count',
        'results', 'is_featured', 'is_active', 'order'
    ]
    template_name = 'dashboards/crud/projects/project_form.html'
    success_url = reverse_lazy('dashboards:project_list')
    success_message = "Проект успешно обновлен"

class ProjectDeleteView(BaseAdminDeleteView):
    model = Project
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:project_list')
    success_message = "Проект удален"

# ---------------------- ProjectMember ----------------------
class ProjectMemberListView(BaseAdminListView):
    model = ProjectMember
    template_name = 'dashboards/crud/projects/projectmember_list.html'
    context_object_name = 'items'

class ProjectMemberCreateView(BaseAdminCreateView):
    model = ProjectMember
    fields = ['project', 'name', 'role', 'organization', 'position', 'email', 'phone', 'is_active']
    template_name = 'dashboards/crud/projects/projectmember_form.html'
    success_url = reverse_lazy('dashboards:projectmember_list')
    success_message = "Участник успешно добавлен"

class ProjectMemberUpdateView(BaseAdminUpdateView):
    model = ProjectMember
    fields = ['project', 'name', 'role', 'organization', 'position', 'email', 'phone', 'is_active']
    template_name = 'dashboards/crud/projects/projectmember_form.html'
    success_url = reverse_lazy('dashboards:projectmember_list')
    success_message = "Участник успешно обновлен"

class ProjectMemberDeleteView(BaseAdminDeleteView):
    model = ProjectMember
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectmember_list')
    success_message = "Участник удален"

# ---------------------- ProjectPartner ----------------------
class ProjectPartnerListView(BaseAdminListView):
    model = ProjectPartner
    template_name = 'dashboards/crud/projects/projectpartner_list.html'
    context_object_name = 'items'

class ProjectPartnerCreateView(BaseAdminCreateView):
    model = ProjectPartner
    fields = ['project', 'name', 'logo', 'website', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectpartner_form.html'
    success_url = reverse_lazy('dashboards:projectpartner_list')
    success_message = "Партнер успешно добавлен"

class ProjectPartnerUpdateView(BaseAdminUpdateView):
    model = ProjectPartner
    fields = ['project', 'name', 'logo', 'website', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectpartner_form.html'
    success_url = reverse_lazy('dashboards:projectpartner_list')
    success_message = "Партнер успешно обновлен"

class ProjectPartnerDeleteView(BaseAdminDeleteView):
    model = ProjectPartner
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectpartner_list')
    success_message = "Партнер удален"

# ---------------------- ProjectSlide ----------------------
class ProjectSlideListView(BaseAdminListView):
    model = ProjectSlide
    template_name = 'dashboards/crud/projects/projectslide_list.html'
    context_object_name = 'items'

class ProjectSlideCreateView(BaseAdminCreateView):
    model = ProjectSlide
    fields = ['title', 'image', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectslide_form.html'
    success_url = reverse_lazy('dashboards:projectslide_list')
    success_message = "Слайд успешно добавлен"

class ProjectSlideUpdateView(BaseAdminUpdateView):
    model = ProjectSlide
    fields = ['title', 'image', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectslide_form.html'
    success_url = reverse_lazy('dashboards:projectslide_list')
    success_message = "Слайд успешно обновлен"

class ProjectSlideDeleteView(BaseAdminDeleteView):
    model = ProjectSlide
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectslide_list')
    success_message = "Слайд удален"

# ---------------------- ContactRequest ----------------------
class ContactRequestListView(BaseAdminListView):
    model = ContactRequest
    template_name = 'dashboards/crud/projects/contactrequest_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ContactRequestUpdateView(BaseAdminUpdateView):
    model = ContactRequest
    fields = ['is_processed']
    template_name = 'dashboards/crud/projects/contactrequest_form.html'
    success_url = reverse_lazy('dashboards:contactrequest_list')
    success_message = "Запрос обновлен"

class ContactRequestDeleteView(BaseAdminDeleteView):
    model = ContactRequest
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:contactrequest_list')
    success_message = "Запрос удален"

# ---------------------- ProjectProposal ----------------------
class ProjectProposalListView(BaseAdminListView):
    model = ProjectProposal
    template_name = 'dashboards/crud/projects/projectproposal_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ProjectProposalUpdateView(BaseAdminUpdateView):
    model = ProjectProposal
    fields = ['status']
    template_name = 'dashboards/crud/projects/projectproposal_form.html'
    success_url = reverse_lazy('dashboards:projectproposal_list')
    success_message = "Предложение обновлено"

class ProjectProposalDeleteView(BaseAdminDeleteView):
    model = ProjectProposal
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectproposal_list')
    success_message = "Предложение удалено"

# ---------------------- ProjectGallery ----------------------
class ProjectGalleryListView(BaseAdminListView):
    model = ProjectGallery
    template_name = 'dashboards/crud/projects/projectgallery_list.html'
    context_object_name = 'items'

class ProjectGalleryCreateView(BaseAdminCreateView):
    model = ProjectGallery
    fields = ['title', 'image', 'description', 'project', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectgallery_form.html'
    success_url = reverse_lazy('dashboards:projectgallery_list')
    success_message = "Изображение успешно добавлено"

class ProjectGalleryUpdateView(BaseAdminUpdateView):
    model = ProjectGallery
    fields = ['title', 'image', 'description', 'project', 'order', 'is_active']
    template_name = 'dashboards/crud/projects/projectgallery_form.html'
    success_url = reverse_lazy('dashboards:projectgallery_list')
    success_message = "Изображение успешно обновлено"

class ProjectGalleryDeleteView(BaseAdminDeleteView):
    model = ProjectGallery
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectgallery_list')
    success_message = "Изображение удалено"

# ---------------------- ProjectJoinRequest ----------------------
class ProjectJoinRequestListView(BaseAdminListView):
    model = ProjectJoinRequest
    template_name = 'dashboards/crud/projects/projectjoinrequest_list.html'
    context_object_name = 'items'
    paginate_by = 20

class ProjectJoinRequestUpdateView(BaseAdminUpdateView):
    model = ProjectJoinRequest
    fields = ['status']
    template_name = 'dashboards/crud/projects/projectjoinrequest_form.html'
    success_url = reverse_lazy('dashboards:projectjoinrequest_list')
    success_message = "Запрос обновлен"

class ProjectJoinRequestDeleteView(BaseAdminDeleteView):
    model = ProjectJoinRequest
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:projectjoinrequest_list')
    success_message = "Запрос удален"