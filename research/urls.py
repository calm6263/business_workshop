from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research_list, name='research_list'),
    path('categories/', views.research_categories, name='research_categories'),
    path('<int:research_id>/', views.research_detail, name='research_detail'),
    path('conferences/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conferences/<int:conference_id>/register/', views.conference_registration, name='conference_registration'),
    path('youth-council/<int:pk>/detail/', views.youth_council_member_detail, name='youth_council_detail'),
]