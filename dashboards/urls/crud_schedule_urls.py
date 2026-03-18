from django.urls import path
from ..views import crud_schedule

urlpatterns = [
    # ScheduleProgram
    path('programs/', crud_schedule.ScheduleProgramListView.as_view(), name='scheduleprogram_list'),
    path('programs/add/', crud_schedule.ScheduleProgramCreateView.as_view(), name='scheduleprogram_add'),
    path('programs/<int:pk>/edit/', crud_schedule.ScheduleProgramUpdateView.as_view(), name='scheduleprogram_edit'),
    path('programs/<int:pk>/delete/', crud_schedule.ScheduleProgramDeleteView.as_view(), name='scheduleprogram_delete'),

    # CurriculumModule
    path('modules/', crud_schedule.CurriculumModuleListView.as_view(), name='curriculummodule_list'),
    path('modules/add/', crud_schedule.CurriculumModuleCreateView.as_view(), name='curriculummodule_add'),
    path('modules/<int:pk>/edit/', crud_schedule.CurriculumModuleUpdateView.as_view(), name='curriculummodule_edit'),
    path('modules/<int:pk>/delete/', crud_schedule.CurriculumModuleDeleteView.as_view(), name='curriculummodule_delete'),

    # CurriculumDocument
    path('documents/', crud_schedule.CurriculumDocumentListView.as_view(), name='curriculumdocument_list'),
    path('documents/add/', crud_schedule.CurriculumDocumentCreateView.as_view(), name='curriculumdocument_add'),
    path('documents/<int:pk>/edit/', crud_schedule.CurriculumDocumentUpdateView.as_view(), name='curriculumdocument_edit'),
    path('documents/<int:pk>/delete/', crud_schedule.CurriculumDocumentDeleteView.as_view(), name='curriculumdocument_delete'),

    # ProgramApplication
    path('applications/', crud_schedule.ProgramApplicationListView.as_view(), name='programapplication_list'),
    path('applications/add/', crud_schedule.ProgramApplicationCreateView.as_view(), name='programapplication_add'),
    path('applications/<int:pk>/edit/', crud_schedule.ProgramApplicationUpdateView.as_view(), name='programapplication_edit'),
    path('applications/<int:pk>/delete/', crud_schedule.ProgramApplicationDeleteView.as_view(), name='programapplication_delete'),

    # ScheduleSliderImage
    path('schedule-slider/', crud_schedule.ScheduleSliderImageListView.as_view(), name='schedulesliderimage_list'),
    path('schedule-slider/add/', crud_schedule.ScheduleSliderImageCreateView.as_view(), name='schedulesliderimage_add'),
    path('schedule-slider/<int:pk>/edit/', crud_schedule.ScheduleSliderImageUpdateView.as_view(), name='schedulesliderimage_edit'),
    path('schedule-slider/<int:pk>/delete/', crud_schedule.ScheduleSliderImageDeleteView.as_view(), name='schedulesliderimage_delete'),

    # CalendarSliderImage
    path('calendar-slider/', crud_schedule.CalendarSliderImageListView.as_view(), name='calendarsliderimage_list'),
    path('calendar-slider/add/', crud_schedule.CalendarSliderImageCreateView.as_view(), name='calendarsliderimage_add'),
    path('calendar-slider/<int:pk>/edit/', crud_schedule.CalendarSliderImageUpdateView.as_view(), name='calendarsliderimage_edit'),
    path('calendar-slider/<int:pk>/delete/', crud_schedule.CalendarSliderImageDeleteView.as_view(), name='calendarsliderimage_delete'),
]