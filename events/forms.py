# events/forms.py
from django import forms
from .models import EventRegistration, NewsletterSubscription

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['full_name', 'phone', 'email', 'agreement']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # يمكن إضافة تحقق مخصص لرقم الهاتف
        if not phone.isdigit() and not phone.startswith('+'):
            raise forms.ValidationError("رقم الهاتف يجب أن يحتوي على أرقام فقط أو يبدأ بـ +")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # التحقق من صحة البريد الإلكتروني (Django يقوم بذلك تلقائياً)
        return email

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'agreement']