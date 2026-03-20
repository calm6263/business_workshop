# dashboards/urls/crud_urls.py
from django.urls import path
from ..views import crud_views

urlpatterns = [
    # MainSlider
    path('main-slider/', crud_views.MainSliderListView.as_view(), name='main_slider_list'),
    path('main-slider/add/', crud_views.MainSliderCreateView.as_view(), name='main_slider_add'),
    path('main-slider/<int:pk>/edit/', crud_views.MainSliderUpdateView.as_view(), name='main_slider_edit'),
    path('main-slider/<int:pk>/delete/', crud_views.MainSliderDeleteView.as_view(), name='main_slider_delete'),

    # ValuesSection
    path('values/', crud_views.ValuesSectionListView.as_view(), name='values_list'),
    path('values/add/', crud_views.ValuesSectionCreateView.as_view(), name='values_add'),
    path('values/<int:pk>/edit/', crud_views.ValuesSectionUpdateView.as_view(), name='values_edit'),
    path('values/<int:pk>/delete/', crud_views.ValuesSectionDeleteView.as_view(), name='values_delete'),

    # StatisticsSection
    path('statistics/', crud_views.StatisticsSectionListView.as_view(), name='statistics_list'),
    path('statistics/add/', crud_views.StatisticsSectionCreateView.as_view(), name='statistics_add'),
    path('statistics/<int:pk>/edit/', crud_views.StatisticsSectionUpdateView.as_view(), name='statistics_edit'),
    path('statistics/<int:pk>/delete/', crud_views.StatisticsSectionDeleteView.as_view(), name='statistics_delete'),

    # LeaderSpeech
    path('leader-speech/', crud_views.LeaderSpeechListView.as_view(), name='leaderspeech_list'),
    path('leader-speech/add/', crud_views.LeaderSpeechCreateView.as_view(), name='leaderspeech_add'),
    path('leader-speech/<int:pk>/edit/', crud_views.LeaderSpeechUpdateView.as_view(), name='leaderspeech_edit'),
    path('leader-speech/<int:pk>/delete/', crud_views.LeaderSpeechDeleteView.as_view(), name='leaderspeech_delete'),

    # LeaderSpeechVideo
    path('leader-speech-videos/', crud_views.LeaderSpeechVideoListView.as_view(), name='leaderspeechvideo_list'),
    path('leader-speech-videos/add/', crud_views.LeaderSpeechVideoCreateView.as_view(), name='leaderspeechvideo_add'),
    path('leader-speech-videos/<int:pk>/edit/', crud_views.LeaderSpeechVideoUpdateView.as_view(), name='leaderspeechvideo_edit'),
    path('leader-speech-videos/<int:pk>/delete/', crud_views.LeaderSpeechVideoDeleteView.as_view(), name='leaderspeechvideo_delete'),

    # PhotoAlbum
    path('photo-albums/', crud_views.PhotoAlbumListView.as_view(), name='photoalbum_list'),
    path('photo-albums/add/', crud_views.PhotoAlbumCreateView.as_view(), name='photoalbum_add'),
    path('photo-albums/<int:pk>/edit/', crud_views.PhotoAlbumUpdateView.as_view(), name='photoalbum_edit'),
    path('photo-albums/<int:pk>/delete/', crud_views.PhotoAlbumDeleteView.as_view(), name='photoalbum_delete'),

    # GalleryImage (صور الألبوم)
    path('gallery-images/', crud_views.GalleryImageListView.as_view(), name='galleryimage_list'),
    path('gallery-images/add/', crud_views.GalleryImageCreateView.as_view(), name='galleryimage_add'),
    path('gallery-images/<int:pk>/edit/', crud_views.GalleryImageUpdateView.as_view(), name='galleryimage_edit'),
    path('gallery-images/<int:pk>/delete/', crud_views.GalleryImageDeleteView.as_view(), name='galleryimage_delete'),

    # DownloadableFile
    path('downloadable-files/', crud_views.DownloadableFileListView.as_view(), name='downloadablefile_list'),
    path('downloadable-files/add/', crud_views.DownloadableFileCreateView.as_view(), name='downloadablefile_add'),
    path('downloadable-files/<int:pk>/edit/', crud_views.DownloadableFileUpdateView.as_view(), name='downloadablefile_edit'),
    path('downloadable-files/<int:pk>/delete/', crud_views.DownloadableFileDeleteView.as_view(), name='downloadablefile_delete'),

    # QuoteSection
    path('quotes/', crud_views.QuoteSectionListView.as_view(), name='quotesection_list'),
    path('quotes/add/', crud_views.QuoteSectionCreateView.as_view(), name='quotesection_add'),
    path('quotes/<int:pk>/edit/', crud_views.QuoteSectionUpdateView.as_view(), name='quotesection_edit'),
    path('quotes/<int:pk>/delete/', crud_views.QuoteSectionDeleteView.as_view(), name='quotesection_delete'),

    # Leadership
    path('leadership/', crud_views.LeadershipListView.as_view(), name='leadership_list'),
    path('leadership/add/', crud_views.LeadershipCreateView.as_view(), name='leadership_add'),
    path('leadership/<int:pk>/edit/', crud_views.LeadershipUpdateView.as_view(), name='leadership_edit'),
    path('leadership/<int:pk>/delete/', crud_views.LeadershipDeleteView.as_view(), name='leadership_delete'),

    # AcademyTeamMember
    path('team/', crud_views.AcademyTeamMemberListView.as_view(), name='team_list'),
    path('team/add/', crud_views.AcademyTeamMemberCreateView.as_view(), name='team_add'),
    path('team/<int:pk>/edit/', crud_views.AcademyTeamMemberUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', crud_views.AcademyTeamMemberDeleteView.as_view(), name='team_delete'),
]