from django.shortcuts import render
from .models import ContactSection, OrganizationInfo, SocialMedia, ContactPageSettings, ContactHero

def contacts_page(request):
    contact_sections = ContactSection.objects.filter(is_active=True).order_by('order')
    organization_info = OrganizationInfo.objects.first()
    social_media = SocialMedia.objects.filter(is_active=True).order_by('order')
    page_settings = ContactPageSettings.objects.first()
    
    # تحقق من أننا نحصل على contact_hero
    contact_hero = ContactHero.objects.filter(is_active=True).first()
    
    # أضف طباعة للتشخيص
    print(f"contact_hero found: {contact_hero}")
    if contact_hero:
        print(f"contact_hero image: {contact_hero.image}")
        print(f"contact_hero image URL: {contact_hero.image.url if contact_hero.image else 'No image'}")
    
    # Если настроек нет, создаем по умолчанию
    if not page_settings:
        page_settings = ContactPageSettings.objects.create()
    
    context = {
        'contact_sections': contact_sections,
        'organization_info': organization_info,
        'social_media': social_media,
        'page_settings': page_settings,
        'contact_hero': contact_hero,
    }
    
    return render(request, 'contacts/contacts.html', context)