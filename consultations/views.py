# views.py
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_deny
from .models import ConsultationRequest, HeroSlide, FAQ, SuccessPageImage
from .forms import ConsultationRequestForm

logger = logging.getLogger(__name__)

@csrf_protect
@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
@xframe_options_deny
def consultation_form(request):
    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            try:
                consultation = form.save()
                
                logger.info(
                    f'Заявка на консультацию создана: ID={consultation.request_id}, '
                    f'Email={consultation.contact_email}, '
                    f'Направление={consultation.direction}, '
                    f'IP={request.META.get("REMOTE_ADDR", "Неизвестно")}'
                )
                
                # Redirect to success page
                return redirect('consultations:success')
                
            except Exception as e:
                logger.error(
                    f'Ошибка при создании заявки: {str(e)}, '
                    f'IP={request.META.get("REMOTE_ADDR", "Неизвестно")}, '
                    f'User-Agent={request.META.get("HTTP_USER_AGENT", "Неизвестно")}'
                )
                messages.error(request, 'Произошла ошибка при сохранении заявки. Пожалуйста, попробуйте еще раз.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    safe_error = str(error)  # سيتم تصريفه تلقائياً في القالب
                    field_display = dict(form.fields).get(field, field).label or field
                    messages.error(request, f"{field_display}: {safe_error}")
            
            logger.warning(
                f'Неудачная попытка отправки формы: {form.errors}, '
                f'IP={request.META.get("REMOTE_ADDR", "Неизвестно")}, '
                f'User-Agent={request.META.get("HTTP_USER_AGENT", "Неизвестно")}'
            )
    else:
        form = ConsultationRequestForm()
    
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    
    logger.info(
        f'Посещение страницы консультаций: '
        f'IP={request.META.get("REMOTE_ADDR", "Неизвестно")}, '
        f'User-Agent={request.META.get("HTTP_USER_AGENT", "Неизвестно")}'
    )
    
    return render(request, 'consultations/consultation_form.html', {
        'form': form,
        'hero_slides': hero_slides,  # تمرير البيانات مباشرة دون تعديل
        'faqs': faqs,
        'current_year': timezone.now().year,
    })

def success(request):
    success_image = SuccessPageImage.objects.filter(is_active=True).first()
    return render(request, 'consultations/success.html', {
        'success_image': success_image,
        'current_year': timezone.now().year,
    })