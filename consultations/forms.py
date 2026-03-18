from django import forms
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from .models import ConsultationRequest

class ConsultationRequestForm(forms.ModelForm):
    contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '(___) ___-____',
            'class': 'form-control phone-input'
        }),
        validators=[
            RegexValidator(
                regex=r'^\+?7?\d{10,15}$',
                message='Введите корректный номер телефона. Формат: +7XXXXXXXXXX'
            )
        ]
    )
    
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@email.com',
            'class': 'form-control email-input'
        })
    )
    
    class Meta:
        model = ConsultationRequest
        fields = ['direction', 'date', 'time', 'contact_phone', 'contact_email', 'additional_wishes', 'agreed_to_terms']
        widgets = {
            'direction': forms.Select(attrs={
                'class': 'form-control direction-select',
                'placeholder': 'Выберите направление'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control date-input',
                'min': 'today'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control time-input'
            }),
            'additional_wishes': forms.Textarea(attrs={
                'rows': 5, 
                'maxlength': '200',
                'class': 'form-control additional-wishes',
                'placeholder': 'Введите ваши пожелания (максимум 200 символов)'
            }),
            'agreed_to_terms': forms.CheckboxInput(attrs={
                'class': 'form-check-input agreement-checkbox',
                'required': 'required'
            })
        }
        labels = {
            'direction': 'Направление',
            'date': 'Дата',
            'time': 'Время',
            'contact_phone': 'Телефон',
            'contact_email': 'E-mail',
            'additional_wishes': 'Дополнительные пожелания',
            'agreed_to_terms': 'Я согласен с условиями пользовательского соглашения и политикой конфиденциальности',
        }
        
    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if not phone:
            return phone
            
        # تنظيف رقم الهاتف من الرموز الشائعة
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        elif phone.startswith('7'):
            phone = '+' + phone
        elif not phone.startswith('+'):
            phone = '+7' + phone
            
        # تحقق إضافي من صحة الرقم
        if not phone.startswith('+7') or len(phone) < 12:
            raise ValidationError('Введите корректный номер телефона. Формат: +7XXXXXXXXXX')
            
        return phone
    
    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        if not email:
            return email
            
        email = email.strip().lower()
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Введите корректный email адрес')
            
        return email
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        from datetime import date as datetime_date
        if date and date < datetime_date.today():
            raise ValidationError('Дата не может быть в прошлом')
        return date
    
    def clean_additional_wishes(self):
        wishes = self.cleaned_data.get('additional_wishes', '')
        # تنظيف النص من XSS (يبقى escape فقط للنصوص الطويلة)
        from django.utils.html import escape
        wishes = escape(wishes.strip())
        return wishes
    
    def clean(self):
        cleaned_data = super().clean()
        
        # تحقق إضافي من موعد المستقبلي
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if date and time:
            from datetime import datetime
            consultation_datetime = datetime.combine(date, time)
            if consultation_datetime < datetime.now():
                raise ValidationError('Время консультации не может быть в прошлом')
        
        return cleaned_data