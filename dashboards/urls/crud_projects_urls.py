from django.urls import path
from ..views import crud_projects

urlpatterns = [
    # ProjectCategory
    path('categories/', crud_projects.ProjectCategoryListView.as_view(), name='projectcategory_list'),
    path('categories/add/', crud_projects.ProjectCategoryCreateView.as_view(), name='projectcategory_add'),
    path('categories/<int:pk>/edit/', crud_projects.ProjectCategoryUpdateView.as_view(), name='projectcategory_edit'),
    path('categories/<int:pk>/delete/', crud_projects.ProjectCategoryDeleteView.as_view(), name='projectcategory_delete'),

    # Project
    path('projects/', crud_projects.ProjectListView.as_view(), name='project_list'),
    path('projects/add/', crud_projects.ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/edit/', crud_projects.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', crud_projects.ProjectDeleteView.as_view(), name='project_delete'),

    # ProjectMember
    path('members/', crud_projects.ProjectMemberListView.as_view(), name='projectmember_list'),
    path('members/add/', crud_projects.ProjectMemberCreateView.as_view(), name='projectmember_add'),
    path('members/<int:pk>/edit/', crud_projects.ProjectMemberUpdateView.as_view(), name='projectmember_edit'),
    path('members/<int:pk>/delete/', crud_projects.ProjectMemberDeleteView.as_view(), name='projectmember_delete'),

    # ProjectPartner
    path('partners/', crud_projects.ProjectPartnerListView.as_view(), name='projectpartner_list'),
    path('partners/add/', crud_projects.ProjectPartnerCreateView.as_view(), name='projectpartner_add'),
    path('partners/<int:pk>/edit/', crud_projects.ProjectPartnerUpdateView.as_view(), name='projectpartner_edit'),
    path('partners/<int:pk>/delete/', crud_projects.ProjectPartnerDeleteView.as_view(), name='projectpartner_delete'),

    # ProjectSlide
    path('slides/', crud_projects.ProjectSlideListView.as_view(), name='projectslide_list'),
    path('slides/add/', crud_projects.ProjectSlideCreateView.as_view(), name='projectslide_add'),
    path('slides/<int:pk>/edit/', crud_projects.ProjectSlideUpdateView.as_view(), name='projectslide_edit'),
    path('slides/<int:pk>/delete/', crud_projects.ProjectSlideDeleteView.as_view(), name='projectslide_delete'),

    # ContactRequest
    path('contact-requests/', crud_projects.ContactRequestListView.as_view(), name='contactrequest_list'),
    path('contact-requests/<int:pk>/edit/', crud_projects.ContactRequestUpdateView.as_view(), name='contactrequest_edit'),
    path('contact-requests/<int:pk>/delete/', crud_projects.ContactRequestDeleteView.as_view(), name='contactrequest_delete'),

    # ProjectProposal
    path('proposals/', crud_projects.ProjectProposalListView.as_view(), name='projectproposal_list'),
    path('proposals/<int:pk>/edit/', crud_projects.ProjectProposalUpdateView.as_view(), name='projectproposal_edit'),
    path('proposals/<int:pk>/delete/', crud_projects.ProjectProposalDeleteView.as_view(), name='projectproposal_delete'),

    # ProjectGallery
    path('gallery/', crud_projects.ProjectGalleryListView.as_view(), name='projectgallery_list'),
    path('gallery/add/', crud_projects.ProjectGalleryCreateView.as_view(), name='projectgallery_add'),
    path('gallery/<int:pk>/edit/', crud_projects.ProjectGalleryUpdateView.as_view(), name='projectgallery_edit'),
    path('gallery/<int:pk>/delete/', crud_projects.ProjectGalleryDeleteView.as_view(), name='projectgallery_delete'),

    # ProjectJoinRequest
    path('join-requests/', crud_projects.ProjectJoinRequestListView.as_view(), name='projectjoinrequest_list'),
    path('join-requests/<int:pk>/edit/', crud_projects.ProjectJoinRequestUpdateView.as_view(), name='projectjoinrequest_edit'),
    path('join-requests/<int:pk>/delete/', crud_projects.ProjectJoinRequestDeleteView.as_view(), name='projectjoinrequest_delete'),
]