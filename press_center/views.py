from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import PressCenterPage, PublicationRequest
from research.models import Research

def press_center(request):
    press_page = PressCenterPage.objects.filter(is_active=True).first()
    additional_images = []
    if press_page:
        additional_images = press_page.images.all().order_by('order')
    research_list = Research.objects.filter(is_active=True).order_by('-publication_date')[:6]

    context = {
        'press_page': press_page,
        'additional_images': additional_images,
        'research_list': research_list,
        'isAuthenticated': request.user.is_authenticated,   # مهم لتفعيل النافذة حسب حالة المستخدم
    }
    return render(request, 'press_center/press_center.html', context)


@require_POST
def submit_publication_request(request):
    # التحقق من تسجيل الدخول
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Необходимо авторизоваться.'
        }, status=403)

    # التحقق من نوع المستخدم (فقط عادي، طالب، شركة)
    allowed_types = ['regular', 'student', 'company']
    if not hasattr(request.user, 'profile') or request.user.profile.user_type not in allowed_types:
        return JsonResponse({
            'success': False,
            'message': 'У вас нет прав для подачи заявки.'
        }, status=403)

    try:
        data = json.loads(request.body)

        required_fields = ['organization', 'theme', 'desired_dates', 'contact_person', 'phone', 'email']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Поле {field} обязательно для заполнения'
                }, status=400)

        email = data.get('email', '').strip()
        if '@' not in email or '.' not in email:
            return JsonResponse({
                'success': False,
                'message': 'Пожалуйста, введите корректный адрес электронной почты'
            }, status=400)

        publication_request = PublicationRequest(
            organization=data.get('organization', '').strip(),
            theme=data.get('theme', '').strip(),
            desired_dates=data.get('desired_dates', '').strip(),
            contact_person=data.get('contact_person', '').strip(),
            phone=data.get('phone', '').strip(),
            email=email,
            additional_wishes=data.get('additional_wishes', '').strip()
        )
        publication_request.save()

        return JsonResponse({
            'success': True,
            'message': 'Заявка успешно отправлена!',
            'request_number': publication_request.request_number
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ошибка при отправке заявки: {str(e)}'
        }, status=400)