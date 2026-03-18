from django.urls import path
from ..views import crud_fta_journal

urlpatterns = [
    # JournalIssue
    path('issues/', crud_fta_journal.JournalIssueListView.as_view(), name='journalissue_list'),
    path('issues/add/', crud_fta_journal.JournalIssueCreateView.as_view(), name='journalissue_add'),
    path('issues/<int:pk>/edit/', crud_fta_journal.JournalIssueUpdateView.as_view(), name='journalissue_edit'),
    path('issues/<int:pk>/delete/', crud_fta_journal.JournalIssueDeleteView.as_view(), name='journalissue_delete'),

    # SliderImage
    path('slider/', crud_fta_journal.SliderImageListView.as_view(), name='sliderimage_list'),
    path('slider/add/', crud_fta_journal.SliderImageCreateView.as_view(), name='sliderimage_add'),
    path('slider/<int:pk>/edit/', crud_fta_journal.SliderImageUpdateView.as_view(), name='sliderimage_edit'),
    path('slider/<int:pk>/delete/', crud_fta_journal.SliderImageDeleteView.as_view(), name='sliderimage_delete'),

    # SectionSettings (singleton)
    path('settings/', crud_fta_journal.SectionSettingsListView.as_view(), name='sectionsettings_list'),
    path('settings/add/', crud_fta_journal.SectionSettingsCreateView.as_view(), name='sectionsettings_add'),
    path('settings/<int:pk>/edit/', crud_fta_journal.SectionSettingsUpdateView.as_view(), name='sectionsettings_edit'),
    path('settings/<int:pk>/delete/', crud_fta_journal.SectionSettingsDeleteView.as_view(), name='sectionsettings_delete'),

    # IssuePage
    path('pages/', crud_fta_journal.IssuePageListView.as_view(), name='issuepage_list'),
    path('pages/add/', crud_fta_journal.IssuePageCreateView.as_view(), name='issuepage_add'),
    path('pages/<int:pk>/edit/', crud_fta_journal.IssuePageUpdateView.as_view(), name='issuepage_edit'),
    path('pages/<int:pk>/delete/', crud_fta_journal.IssuePageDeleteView.as_view(), name='issuepage_delete'),
]