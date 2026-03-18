# dashboards/urls/crud_staff_urls.py
from django.urls import path
from ..views import crud_staff

urlpatterns = [
    # TeamMember
    path('members/', crud_staff.TeamMemberListView.as_view(), name='teammember_list'),
    path('members/add/', crud_staff.TeamMemberCreateView.as_view(), name='teammember_add'),
    path('members/<int:pk>/edit/', crud_staff.TeamMemberUpdateView.as_view(), name='teammember_edit'),
    path('members/<int:pk>/delete/', crud_staff.TeamMemberDeleteView.as_view(), name='teammember_delete'),

    # TeacherProgram
    path('programs/', crud_staff.TeacherProgramListView.as_view(), name='teacherprogram_list'),
    path('programs/add/', crud_staff.TeacherProgramCreateView.as_view(), name='teacherprogram_add'),
    path('programs/<int:pk>/edit/', crud_staff.TeacherProgramUpdateView.as_view(), name='teacherprogram_edit'),
    path('programs/<int:pk>/delete/', crud_staff.TeacherProgramDeleteView.as_view(), name='teacherprogram_delete'),

    # PageHero
    path('hero/', crud_staff.PageHeroListView.as_view(), name='pagehero_list'),
    path('hero/add/', crud_staff.PageHeroCreateView.as_view(), name='pagehero_add'),
    path('hero/<int:pk>/edit/', crud_staff.PageHeroUpdateView.as_view(), name='pagehero_edit'),
    path('hero/<int:pk>/delete/', crud_staff.PageHeroDeleteView.as_view(), name='pagehero_delete'),
]