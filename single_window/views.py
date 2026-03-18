from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import BasicInfo, FAQ, ServiceRequest, Slider

def single_window_services(request):
    basic_info = BasicInfo.objects.first()
    
    if not basic_info:
        basic_info = BasicInfo()
    
    # Получить активные слайдеры
    slider_images = Slider.objects.filter(is_active=True).order_by('order')
    
    context = {
        'basic_info': basic_info,
        'slider_images': slider_images,
    }
    return render(request, 'single_window/single_window_services.html', context)

def service_detail(request, slug):
    # Получить активные слайдеры (نفس السلايدر المستخدم في الصفحة الرئيسية)
    slider_images = Slider.objects.filter(is_active=True).order_by('order')
    
    # Список услуг с содержимым
    services_content = {
        'oformit-spravku': {
            'name': 'Оформить справку',
            'description': 'Оформление различных справок для студентов и сотрудников',
            'service_type': 'oformit-spravku'
        },
        'poluchit-dokumenty': {
            'name': 'Оформить стипендию',
            'description': 'Оформление стипендии для студентов',
            'service_type': 'poluchit-dokumenty'
        },
        'poluchit-materialnuyu-podderzhku': {
            'name': 'Целевое обучение',
            'description': 'Оформление целевого обучения',
            'service_type': 'poluchit-materialnuyu-podderzhku'
        },
        'napravit-materinskiy-kapital': {
            'name': 'Дополнительные платформы для обучающихся',
            'description': 'Предоставление доступа к дополнительным образовательным платформам',
            'service_type': 'napravit-materinskiy-kapital'
        },
        'oformit-chitatelskiy-bilet': {
            'name': 'Оформить читательский билет',
            'description': 'Оформление читательского билета для библиотеки',
            'service_type': 'oformit-chitatelskiy-bilet'
        },
        'izmenit-lichnye-dannye': {
            'name': 'Получить закрывающие документы',
            'description': 'Получение закрывающих документов об окончании обучения',
            'service_type': 'izmenit-lichnye-dannye'
        },
        'obrazovatelnyy-kredit': {
            'name': 'Получить льготу на образование',
            'description': 'Оформление льготы на образовательные услуги',
            'service_type': 'obrazovatelnyy-kredit'
        },
        'poluchit-lgotu': {
            'name': 'Восстановление документа об образовании',
            'description': 'Восстановление утерянных документов об образовании',
            'service_type': 'poluchit-lgotu'
        }
    }
    
    service = services_content.get(slug)
    
    if not service:
        return redirect('single_window:single_window_services')
    
    # Получить FAQ из базы данных
    service_type = service['service_type']
    faqs = FAQ.objects.filter(
        service=service_type, 
        is_active=True
    ).order_by('question_number')
    
    # Проверить предыдущие запросы пользователя
    user_requests = []
    if request.user.is_authenticated:
        user_requests = ServiceRequest.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
    
    context = {
        'service': service,
        'faqs': faqs,
        'user_requests': user_requests,
        'slider_images': slider_images,  # إضافة السلايدر للقائمة
    }
    return render(request, 'single_window/service_detail.html', context)

@login_required
@csrf_exempt
@require_POST
def submit_service_request(request):
    try:
        data = json.loads(request.body)
        
        # Создать новую заявку на услугу
        service_request = ServiceRequest(
            service_type=data.get('service_type'),
            format=data.get('format', ''),
            contact_person=data.get('contact_person'),
            phone=data.get('phone'),
            email=request.user.email,  # Использовать email зарегистрированного пользователя
            additional_info=data.get('additional_info', ''),
            agreed_to_terms=data.get('agreed_to_terms', False),
            user=request.user  # Связать заявку с пользователем
        )
        service_request.save()
        
        return JsonResponse({
            'success': True,
            'request_number': service_request.request_number,
            'message': 'Заявка успешно отправлена'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def my_service_requests(request):
    """Показать заявки на услуги пользователя"""
    user_requests = ServiceRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'user_requests': user_requests
    }
    return render(request, 'single_window/my_requests.html', context)