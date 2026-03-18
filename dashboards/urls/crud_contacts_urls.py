from django.urls import path
from ..views import crud_contacts

urlpatterns = [
    # ContactSection
    path('sections/', crud_contacts.ContactSectionListView.as_view(), name='contactsection_list'),
    path('sections/add/', crud_contacts.ContactSectionCreateView.as_view(), name='contactsection_add'),
    path('sections/<int:pk>/edit/', crud_contacts.ContactSectionUpdateView.as_view(), name='contactsection_edit'),
    path('sections/<int:pk>/delete/', crud_contacts.ContactSectionDeleteView.as_view(), name='contactsection_delete'),

    # OrganizationInfo (singleton)
    path('organization/', crud_contacts.OrganizationInfoListView.as_view(), name='organizationinfo_list'),
    path('organization/add/', crud_contacts.OrganizationInfoCreateView.as_view(), name='organizationinfo_add'),
    path('organization/<int:pk>/edit/', crud_contacts.OrganizationInfoUpdateView.as_view(), name='organizationinfo_edit'),
    path('organization/<int:pk>/delete/', crud_contacts.OrganizationInfoDeleteView.as_view(), name='organizationinfo_delete'),

    # SocialMedia
    path('social/', crud_contacts.SocialMediaListView.as_view(), name='socialmedia_list'),
    path('social/add/', crud_contacts.SocialMediaCreateView.as_view(), name='socialmedia_add'),
    path('social/<int:pk>/edit/', crud_contacts.SocialMediaUpdateView.as_view(), name='socialmedia_edit'),
    path('social/<int:pk>/delete/', crud_contacts.SocialMediaDeleteView.as_view(), name='socialmedia_delete'),

    # ContactPageSettings (singleton)
    path('settings/', crud_contacts.ContactPageSettingsListView.as_view(), name='contactpagesettings_list'),
    path('settings/add/', crud_contacts.ContactPageSettingsCreateView.as_view(), name='contactpagesettings_add'),
    path('settings/<int:pk>/edit/', crud_contacts.ContactPageSettingsUpdateView.as_view(), name='contactpagesettings_edit'),
    path('settings/<int:pk>/delete/', crud_contacts.ContactPageSettingsDeleteView.as_view(), name='contactpagesettings_delete'),

    # ContactHero
    path('hero/', crud_contacts.ContactHeroListView.as_view(), name='contacthero_list'),
    path('hero/add/', crud_contacts.ContactHeroCreateView.as_view(), name='contacthero_add'),
    path('hero/<int:pk>/edit/', crud_contacts.ContactHeroUpdateView.as_view(), name='contacthero_edit'),
    path('hero/<int:pk>/delete/', crud_contacts.ContactHeroDeleteView.as_view(), name='contacthero_delete'),
]