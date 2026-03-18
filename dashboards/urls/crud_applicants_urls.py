from django.urls import path
from ..views import crud_applicants

urlpatterns = [
    # ApplicantsPage
    path('page/', crud_applicants.ApplicantsPageListView.as_view(), name='applicantspage_list'),
    path('page/add/', crud_applicants.ApplicantsPageCreateView.as_view(), name='applicantspage_add'),
    path('page/<int:pk>/edit/', crud_applicants.ApplicantsPageUpdateView.as_view(), name='applicantspage_edit'),
    path('page/<int:pk>/delete/', crud_applicants.ApplicantsPageDeleteView.as_view(), name='applicantspage_delete'),

    # ApplicationMethod
    path('methods/', crud_applicants.ApplicationMethodListView.as_view(), name='applicationmethod_list'),
    path('methods/add/', crud_applicants.ApplicationMethodCreateView.as_view(), name='applicationmethod_add'),
    path('methods/<int:pk>/edit/', crud_applicants.ApplicationMethodUpdateView.as_view(), name='applicationmethod_edit'),
    path('methods/<int:pk>/delete/', crud_applicants.ApplicationMethodDeleteView.as_view(), name='applicationmethod_delete'),

    # EnrollmentStage
    path('stages/', crud_applicants.EnrollmentStageListView.as_view(), name='enrollmentstage_list'),
    path('stages/add/', crud_applicants.EnrollmentStageCreateView.as_view(), name='enrollmentstage_add'),
    path('stages/<int:pk>/edit/', crud_applicants.EnrollmentStageUpdateView.as_view(), name='enrollmentstage_edit'),
    path('stages/<int:pk>/delete/', crud_applicants.EnrollmentStageDeleteView.as_view(), name='enrollmentstage_delete'),

    # ApplicantDocument
    path('documents/', crud_applicants.ApplicantDocumentListView.as_view(), name='applicantdocument_list'),
    path('documents/add/', crud_applicants.ApplicantDocumentCreateView.as_view(), name='applicantdocument_add'),
    path('documents/<int:pk>/edit/', crud_applicants.ApplicantDocumentUpdateView.as_view(), name='applicantdocument_edit'),
    path('documents/<int:pk>/delete/', crud_applicants.ApplicantDocumentDeleteView.as_view(), name='applicantdocument_delete'),

    # ApplicantApplication
    path('applications/', crud_applicants.ApplicantApplicationListView.as_view(), name='applicantapplication_list'),
    path('applications/add/', crud_applicants.ApplicantApplicationCreateView.as_view(), name='applicantapplication_add'),
    path('applications/<int:pk>/edit/', crud_applicants.ApplicantApplicationUpdateView.as_view(), name='applicantapplication_edit'),
    path('applications/<int:pk>/delete/', crud_applicants.ApplicantApplicationDeleteView.as_view(), name='applicantapplication_delete'),
]