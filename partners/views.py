from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import re
from .models import Partner, PartnershipApplication, HomePageSlider, LogoCarousel

# تعريف النماذج مباشرة في views.py
class PartnershipApplicationForm(forms.ModelForm):
    class Meta:
        model = PartnershipApplication
        fields = ['application_type', 'company_name', 'inn', 'kpp', 'legal_address', 'comments', 'contact_person', 'phone', 'email']
        widgets = {
            'application_type': forms.HiddenInput(),
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название компании'}),
            'inn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ИНН'}),
            'kpp': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'КПП'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Юридический адрес'}),
            'comments': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Комментарии', 'rows': 4}),
            'contact_person': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Контактное лицо'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Электронная почта'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Удаляем все пробелы, дефисы, скобки, оставляем только цифры и знак +
            cleaned = re.sub(r'[\s\-\(\)]', '', phone)
            # Проверяем, что остались только цифры и возможно один + в начале
            if not re.match(r'^\+?[\d]{10,15}$', cleaned):
                raise forms.ValidationError('Введите корректный номер телефона (от 10 до 15 цифр, допускается + в начале).')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        application_type = cleaned_data.get('application_type')

        if application_type == 'legal':
            inn = cleaned_data.get('inn')
            kpp = cleaned_data.get('kpp')
            legal_address = cleaned_data.get('legal_address')

            if not inn:
                self.add_error('inn', 'Это поле обязательно для юридических лиц')
            if not kpp:
                self.add_error('kpp', 'Это поле обязательно для юридических лиц')
            if not legal_address:
                self.add_error('legal_address', 'Это поле обязательно для юридических лиц')

        return cleaned_data


def partners_list(request):
    sliders = HomePageSlider.objects.filter(is_active=True).order_by('order')
    carousel_partners = Partner.objects.filter(is_active=True, show_in_carousel=True).order_by('order', 'name')
    grid_partners = Partner.objects.filter(is_active=True, show_in_grid=True).order_by('order', 'name')

    if request.method == 'POST' and 'application_type' in request.POST:
        form_data = request.POST.copy()

        if form_data.get('application_type') == 'physical':
            if not form_data.get('company_name'):
                form_data['company_name'] = 'Физическое лицо'
            form_data['inn'] = ''
            form_data['kpp'] = ''
            form_data['legal_address'] = ''

        form = PartnershipApplicationForm(form_data)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Используем транзакцию и блокировку для предотвращения race condition
            with transaction.atomic():
                # Блокируем все записи с таким email за последние 24 часа
                recent_exists = PartnershipApplication.objects.select_for_update().filter(
                    email=email,
                    created_at__gte=timezone.now() - timedelta(hours=24)
                ).exists()

                if recent_exists:
                    messages.error(request, 'Вы уже отправляли заявку за последние 24 часа. Пожалуйста, подождите.')
                    return HttpResponseRedirect(reverse('partners:partners_list'))

                application = form.save()

            success_message = f'Ваша заявка успешно отправлена! Номер вашей заявки: {application.request_number}. Мы свяжемся с вами в ближайшее время.'
            messages.success(request, success_message)
            return HttpResponseRedirect(reverse('partners:partners_list'))
        else:
            # Формируем сообщение об ошибке безопасно (без HTML)
            error_message = 'Пожалуйста, исправьте ошибки в форме:'
            if form.errors:
                error_details = []
                for field, errors in form.errors.items():
                    if field == '__all__':
                        field_name = 'Общие ошибки'
                    else:
                        field_name = dict(form.fields).get(field).label or field
                    error_details.append(f"{field_name}: {', '.join(errors)}")
                error_message += ' ' + '; '.join(error_details)
            messages.error(request, error_message)

    context = {
        'sliders': sliders,
        'carousel_partners': carousel_partners,
        'grid_partners': grid_partners,
    }
    return render(request, 'partners/partners_list.html', context)


def partner_detail(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    return render(request, 'partners/partner_detail.html', {'partner': partner})


def partnership_application(request):
    return HttpResponseRedirect(reverse('partners:partners_list'))