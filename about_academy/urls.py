from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_academy, name='about_academy'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('leadership-detail/', views.leadership_detail, name='leadership_detail'),
    path('team-partial/', views.team_partial, name='team_partial'),
    path('team-member/<int:pk>/detail/', views.academy_team_member_detail, name='academy_team_member_detail'),
]