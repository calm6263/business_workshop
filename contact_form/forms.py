from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message', 'is_robot']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input-small',
                'placeholder': 'Введите ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input-small',
                'placeholder': 'Введите ваш e-mail'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea-small',
                'placeholder': 'Введите ваше сообщение...',
                'rows': 4
            }),
            'is_robot': forms.CheckboxInput(attrs={
                'class': 'form-checkbox-small'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # التحقق من صيغة البريد الإلكتروني باستخدام regex أكثر دقة
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError('Пожалуйста, введите корректный адрес электронной почты.')
        
        # التحقق من أن البريد الإلكتروني ليس مزيفًا
        disposable_domains = ['tempmail.com', 'mailinator.com', '10minutemail.com', 
                             'guerrillamail.com', 'yopmail.com', 'throwawaymail.com']
        domain = email.split('@')[-1].lower()
        
        for disposable in disposable_domains:
            if disposable in domain:
                raise ValidationError('Использование временных адресов электронной почты запрещено.')
        
        return email
    
    def clean_is_robot(self):
        is_robot = self.cleaned_data.get('is_robot')
        if not is_robot:
            raise ValidationError('Пожалуйста, подтвердите, что вы не робот.')
        return is_robot
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        
        # منع الرسائل القصيرة جدًا
        if len(message.strip()) < 10:
            raise ValidationError('Сообщение слишком короткое. Минимальная длина - 10 символов.')
        
        # منع الرسائل الطويلة جدًا
        if len(message) > 2000:
            raise ValidationError('Сообщение слишком длинное. Максимальная длина - 2000 символов.')
        
        return message
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # التحقق من أن الاسم ليس رموزًا عشوائية
        if re.match(r'^[0-9\W_]+$', name):
            raise ValidationError('Пожалуйста, введите корректное имя.')
        
        return name