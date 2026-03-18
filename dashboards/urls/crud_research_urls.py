# dashboards/urls/crud_research_urls.py
from django.urls import path
from ..views import crud_research

urlpatterns = [
    # ResearchCategory
    path('categories/', crud_research.ResearchCategoryListView.as_view(), name='researchcategory_list'),
    path('categories/add/', crud_research.ResearchCategoryCreateView.as_view(), name='researchcategory_add'),
    path('categories/<int:pk>/edit/', crud_research.ResearchCategoryUpdateView.as_view(), name='researchcategory_edit'),
    path('categories/<int:pk>/delete/', crud_research.ResearchCategoryDeleteView.as_view(), name='researchcategory_delete'),

    # Research
    path('research/', crud_research.ResearchListView.as_view(), name='research_list'),
    path('research/add/', crud_research.ResearchCreateView.as_view(), name='research_add'),
    path('research/<int:pk>/edit/', crud_research.ResearchUpdateView.as_view(), name='research_edit'),
    path('research/<int:pk>/delete/', crud_research.ResearchDeleteView.as_view(), name='research_delete'),

    # ResearchTag
    path('tags/', crud_research.ResearchTagListView.as_view(), name='researchtag_list'),
    path('tags/add/', crud_research.ResearchTagCreateView.as_view(), name='researchtag_add'),
    path('tags/<int:pk>/edit/', crud_research.ResearchTagUpdateView.as_view(), name='researchtag_edit'),
    path('tags/<int:pk>/delete/', crud_research.ResearchTagDeleteView.as_view(), name='researchtag_delete'),

    # ResearchHero
    path('hero/', crud_research.ResearchHeroListView.as_view(), name='researchhero_list'),
    path('hero/add/', crud_research.ResearchHeroCreateView.as_view(), name='researchhero_add'),
    path('hero/<int:pk>/edit/', crud_research.ResearchHeroUpdateView.as_view(), name='researchhero_edit'),
    path('hero/<int:pk>/delete/', crud_research.ResearchHeroDeleteView.as_view(), name='researchhero_delete'),

    # Conference
    path('conferences/', crud_research.ConferenceListView.as_view(), name='conference_list'),
    path('conferences/add/', crud_research.ConferenceCreateView.as_view(), name='conference_add'),
    path('conferences/<int:pk>/edit/', crud_research.ConferenceUpdateView.as_view(), name='conference_edit'),
    path('conferences/<int:pk>/delete/', crud_research.ConferenceDeleteView.as_view(), name='conference_delete'),

    # ConferenceRegistration
    path('registrations/', crud_research.ConferenceRegistrationListView.as_view(), name='conferenceregistration_list'),
    path('registrations/add/', crud_research.ConferenceRegistrationCreateView.as_view(), name='conferenceregistration_add'),
    path('registrations/<int:pk>/edit/', crud_research.ConferenceRegistrationUpdateView.as_view(), name='conferenceregistration_edit'),
    path('registrations/<int:pk>/delete/', crud_research.ConferenceRegistrationDeleteView.as_view(), name='conferenceregistration_delete'),

    # YouthCouncilDepartment
    path('youth-departments/', crud_research.YouthCouncilDepartmentListView.as_view(), name='youthcouncildepartment_list'),
    path('youth-departments/add/', crud_research.YouthCouncilDepartmentCreateView.as_view(), name='youthcouncildepartment_add'),
    path('youth-departments/<int:pk>/edit/', crud_research.YouthCouncilDepartmentUpdateView.as_view(), name='youthcouncildepartment_edit'),
    path('youth-departments/<int:pk>/delete/', crud_research.YouthCouncilDepartmentDeleteView.as_view(), name='youthcouncildepartment_delete'),

    # YouthCouncilMember
    path('youth-members/', crud_research.YouthCouncilMemberListView.as_view(), name='youthcouncilmember_list'),
    path('youth-members/add/', crud_research.YouthCouncilMemberCreateView.as_view(), name='youthcouncilmember_add'),
    path('youth-members/<int:pk>/edit/', crud_research.YouthCouncilMemberUpdateView.as_view(), name='youthcouncilmember_edit'),
    path('youth-members/<int:pk>/delete/', crud_research.YouthCouncilMemberDeleteView.as_view(), name='youthcouncilmember_delete'),
]