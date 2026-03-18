# dashboards/urls/crud_partners_urls.py
from django.urls import path
from ..views import crud_partners

urlpatterns = [
    # HomePageSlider
    path('home-slider/', crud_partners.HomePageSliderListView.as_view(), name='homeslider_list'),
    path('home-slider/add/', crud_partners.HomePageSliderCreateView.as_view(), name='homeslider_add'),
    path('home-slider/<int:pk>/edit/', crud_partners.HomePageSliderUpdateView.as_view(), name='homeslider_edit'),
    path('home-slider/<int:pk>/delete/', crud_partners.HomePageSliderDeleteView.as_view(), name='homeslider_delete'),

    # Partner
    path('partners/', crud_partners.PartnerListView.as_view(), name='partner_list'),
    path('partners/add/', crud_partners.PartnerCreateView.as_view(), name='partner_add'),
    path('partners/<int:pk>/edit/', crud_partners.PartnerUpdateView.as_view(), name='partner_edit'),
    path('partners/<int:pk>/delete/', crud_partners.PartnerDeleteView.as_view(), name='partner_delete'),

    # PartnershipApplication
    path('applications/', crud_partners.PartnershipApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/edit/', crud_partners.PartnershipApplicationUpdateView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/', crud_partners.PartnershipApplicationDeleteView.as_view(), name='application_delete'),

    # LogoCarousel
    path('logo-carousel/', crud_partners.LogoCarouselListView.as_view(), name='logocarousel_list'),
    path('logo-carousel/add/', crud_partners.LogoCarouselCreateView.as_view(), name='logocarousel_add'),
    path('logo-carousel/<int:pk>/edit/', crud_partners.LogoCarouselUpdateView.as_view(), name='logocarousel_edit'),
    path('logo-carousel/<int:pk>/delete/', crud_partners.LogoCarouselDeleteView.as_view(), name='logocarousel_delete'),
]