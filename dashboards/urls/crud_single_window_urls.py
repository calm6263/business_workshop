# dashboards/urls/crud_single_window_urls.py
from django.urls import path
from ..views import crud_single_window

urlpatterns = [
    # BasicInfo
    path('basic-info/', crud_single_window.BasicInfoListView.as_view(), name='basicinfo_list'),
    path('basic-info/add/', crud_single_window.BasicInfoCreateView.as_view(), name='basicinfo_add'),
    path('basic-info/<int:pk>/edit/', crud_single_window.BasicInfoUpdateView.as_view(), name='basicinfo_edit'),
    path('basic-info/<int:pk>/delete/', crud_single_window.BasicInfoDeleteView.as_view(), name='basicinfo_delete'),

    # Slider
    path('sliders/', crud_single_window.SliderListView.as_view(), name='slider_list'),
    path('sliders/add/', crud_single_window.SliderCreateView.as_view(), name='slider_add'),
    path('sliders/<int:pk>/edit/', crud_single_window.SliderUpdateView.as_view(), name='slider_edit'),
    path('sliders/<int:pk>/delete/', crud_single_window.SliderDeleteView.as_view(), name='slider_delete'),

    # FAQ
    path('faqs/', crud_single_window.FAQListView.as_view(), name='faq_list'),
    path('faqs/add/', crud_single_window.FAQCreateView.as_view(), name='faq_add'),
    path('faqs/<int:pk>/edit/', crud_single_window.FAQUpdateView.as_view(), name='faq_edit'),
    path('faqs/<int:pk>/delete/', crud_single_window.FAQDeleteView.as_view(), name='faq_delete'),

    # ServiceRequest
    path('requests/', crud_single_window.ServiceRequestListView.as_view(), name='servicerequest_list'),
    path('requests/<int:pk>/edit/', crud_single_window.ServiceRequestUpdateView.as_view(), name='servicerequest_edit'),
    path('requests/<int:pk>/delete/', crud_single_window.ServiceRequestDeleteView.as_view(), name='servicerequest_delete'),
]