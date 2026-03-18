from django.core.management.base import BaseCommand
from contacts.models import ContactSection, OrganizationInfo, ContactPageSettings

class Command(BaseCommand):
    help = 'Load initial contact data'
    
    def handle(self, *args, **options):
        # إنشاء معلومات المنظمة
        OrganizationInfo.objects.get_or_create(
            name='Академия «Пять Башен»',
            defaults={
                'full_name': 'АНО ДПО "Академия «Пять Башен»"',
                'general_phone': '+7 (968) 418-44-88',
                'general_email': 'info.fta@mail.ru',
                'additional_phones': ['+7 (495) 000-00-00'],
                'address': 'Москва, ул. Примерная, д. 123'
            }
        )
        
        # إنشاء أقسام الاتصال
        sections_data = [
            {
                'title': 'Прием документов',
                'section_type': 'documents',
                'phone': '+7 (968) 418-44-88',
                'email': 'info.fta@mail.ru',
                'order': 1
            },
            {
                'title': 'Услуги одного окна',
                'section_type': 'services',
                'phone': '+7 (968) 418-44-88',
                'email': 'info.fta@mail.ru',
                'order': 2
            },
            {
                'title': 'Контакты для СМИ',
                'section_type': 'media',
                'department_name': 'Центр по связям с общественностью',
                'phone': '+7 (968) 418-44-88',
                'email': 'info.fta@mail.ru',
                'order': 3
            },
            {
                'title': 'Техническая поддержка IT',
                'section_type': 'it',
                'department_name': 'Управление цифровой трансформации',
                'phone': '+7 (968) 418-44-88',
                'email': 'info.fta@mail.ru',
                'order': 4
            },
        ]
        
        for section_data in sections_data:
            ContactSection.objects.get_or_create(
                section_type=section_data['section_type'],
                defaults=section_data
            )
        
        # إنشاء إعدادات الصفحة
        ContactPageSettings.objects.get_or_create(
            pk=1,
            defaults={
                'meta_title': 'Контакты - Бизнес-Мастерская',
                'meta_description': 'Контактная информация АНО ДПО Академия «Пять Башен». Телефоны, email, адреса отделов.',
                'show_breadcrumbs': True,
                'show_organization_info': True
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial contact data'))