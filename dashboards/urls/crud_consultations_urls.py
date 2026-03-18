from django.urls import path
from ..views import crud_consultations

urlpatterns = [
    # ConsultationRequest
    path('requests/', crud_consultations.ConsultationRequestListView.as_view(), name='consultationrequest_list'),
    path('requests/<int:pk>/edit/', crud_consultations.ConsultationRequestUpdateView.as_view(), name='consultationrequest_edit'),
    path('requests/<int:pk>/delete/', crud_consultations.ConsultationRequestDeleteView.as_view(), name='consultationrequest_delete'),

    # HeroSlide
    path('hero-slides/', crud_consultations.HeroSlideListView.as_view(), name='heroslide_list'),
    path('hero-slides/add/', crud_consultations.HeroSlideCreateView.as_view(), name='heroslide_add'),
    path('hero-slides/<int:pk>/edit/', crud_consultations.HeroSlideUpdateView.as_view(), name='heroslide_edit'),
    path('hero-slides/<int:pk>/delete/', crud_consultations.HeroSlideDeleteView.as_view(), name='heroslide_delete'),

    # FAQ
    path('faqs/', crud_consultations.FAQListView.as_view(), name='faq_list'),
    path('faqs/add/', crud_consultations.FAQCreateView.as_view(), name='faq_add'),
    path('faqs/<int:pk>/edit/', crud_consultations.FAQUpdateView.as_view(), name='faq_edit'),
    path('faqs/<int:pk>/delete/', crud_consultations.FAQDeleteView.as_view(), name='faq_delete'),

    # SuccessPageImage
    path('success-images/', crud_consultations.SuccessPageImageListView.as_view(), name='successpageimage_list'),
    path('success-images/add/', crud_consultations.SuccessPageImageCreateView.as_view(), name='successpageimage_add'),
    path('success-images/<int:pk>/edit/', crud_consultations.SuccessPageImageUpdateView.as_view(), name='successpageimage_edit'),
    path('success-images/<int:pk>/delete/', crud_consultations.SuccessPageImageDeleteView.as_view(), name='successpageimage_delete'),
]