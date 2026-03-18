from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
import hashlib
from .forms import ContactForm
from .models import ContactMessage

def contact_form_view(request):
    context = {'form': ContactForm(), 'title': 'Форма обратной связи'}
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # التحقق من التكرار بناءً على البريد الإلكتروني
            email = form.cleaned_data['email']
            email_hash = hashlib.sha256(email.lower().encode()).hexdigest()
            
            # التحقق من التكرار في آخر 5 دقائق
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            recent_submissions = ContactMessage.objects.filter(
                email_hash=email_hash,
                created_at__gte=five_minutes_ago
            ).count()
            
            if recent_submissions > 0:
                messages.error(request, 
                    'Вы недавно отправили сообщение. Пожалуйста, подождите 5 минут перед отправкой нового.')
                return render(request, 'contact_form/contact_form.html', {'form': form})
            
            # التحقق من التكرار بناءً على IP
            client_ip = get_client_ip(request)
            if client_ip:
                ip_submissions = ContactMessage.objects.filter(
                    client_ip=client_ip,
                    created_at__gte=five_minutes_ago
                ).count()
                
                if ip_submissions >= 3:
                    messages.error(request,
                        'Превышен лимит отправки сообщений с вашего IP адреса. Пожалуйста, попробуйте позже.')
                    return render(request, 'contact_form/contact_form.html', {'form': form})
            
            # التحقق من التكرار في cache (للمستخدمين بدون JavaScript)
            cache_key = f"contact_form_{email_hash}_{hash(form.cleaned_data['message'])}"
            if cache.get(cache_key):
                messages.error(request,
                    'Это сообщение уже было отправлено. Пожалуйста, подождите несколько минут.')
                return render(request, 'contact_form/contact_form.html', {'form': form})
            
            # حفظ الرسالة
            contact_message = form.save(commit=False)
            contact_message.client_ip = client_ip
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            # تعيين cache لمنع التكرار لمدة 5 دقائق
            cache.set(cache_key, True, 300)
            
            messages.success(request,
                'Спасибо! Ваше сообщение успешно отправлено. Мы ответим вам в ближайшее время.')
            return redirect('contact_form')
        else:
            # جمع كل الأخطاء لعرضها
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    
    return render(request, 'contact_form/contact_form.html', context)

def contact_form_partial(request):
    context = {'form': ContactForm()}
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # نفس التحقق من التكرار كما في view الرئيسي
            email = form.cleaned_data['email']
            email_hash = hashlib.sha256(email.lower().encode()).hexdigest()
            
            five_minutes_ago = timezone.now() - timedelta(minutes=5)
            recent_submissions = ContactMessage.objects.filter(
                email_hash=email_hash,
                created_at__gte=five_minutes_ago
            ).count()
            
            if recent_submissions > 0:
                messages.error(request,
                    'Вы недавно отправили сообщение. Пожалуйста, подождите 5 минут перед отправкой нового.')
                return render(request, 'contact_form/contact_form_partial.html', {'form': form})
            
            client_ip = get_client_ip(request)
            if client_ip:
                ip_submissions = ContactMessage.objects.filter(
                    client_ip=client_ip,
                    created_at__gte=five_minutes_ago
                ).count()
                
                if ip_submissions >= 3:
                    messages.error(request,
                        'Превышен лимит отправки сообщений. Пожалуйста, попробуйте позже.')
                    return render(request, 'contact_form/contact_form_partial.html', {'form': form})
            
            cache_key = f"contact_form_{email_hash}_{hash(form.cleaned_data['message'])}"
            if cache.get(cache_key):
                messages.error(request,
                    'Это сообщение уже было отправлено.')
                return render(request, 'contact_form/contact_form_partial.html', {'form': form})
            
            # حفظ الرسالة
            contact_message = form.save(commit=False)
            contact_message.client_ip = client_ip
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            cache.set(cache_key, True, 300)
            
            # إذا كان الطلب عبر AJAX، نعيد قالب النجاح
            if request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest':
                return render(request, 'contact_form/contact_form_success.html')
            else:
                # إذا لم يكن AJAX، نعيد النموذج الفارغ مع رسالة نجاح
                messages.success(request,
                    'Спасибо! Ваше сообщение успешно отправлено. Мы ответим вам в ближайшее время.')
                return render(request, 'contact_form/contact_form_partial.html', {'form': ContactForm()})
        else:
            # إذا كان هناك أخطاء في التحقق، نعيد النموذج مع الأخطاء
            if request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest':
                return render(request, 'contact_form/contact_form_partial.html', {'form': form})
            else:
                return render(request, 'contact_form/contact_form_partial.html', {'form': form})
    
    return render(request, 'contact_form/contact_form_partial.html', context)

def get_client_ip(request):
    """الحصول على IP العميل"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip