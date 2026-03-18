# applicants/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.db import IntegrityError, OperationalError
import re
import logging
import json
import sys
import traceback
from collections import defaultdict

from .models import ApplicantsPage, ApplicantDocument, ApplicantApplication, ApplicationMethod, EnrollmentStage
from departments.models import Department
from schedule.models import ScheduleProgram
from accounts.models import Profile  # استيراد Profile للتحقق من نوع المستخدم

logger = logging.getLogger(__name__)

# Настройки безопасности
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
PHONE_PATTERN = r'^[\+]?[0-9\s\-\(\)]{10,}$'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def get_client_ip(request):
    """Получение IP-адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def applicants_page(request):
    try:
        documents = ApplicantDocument.objects.filter(is_active=True)
        
        featured_schedule_programs = ScheduleProgram.objects.filter(
            is_active=True
        ).order_by('-created_at')[:2]
        
        departments = Department.objects.filter(is_active=True).order_by('order', 'name')
        
        applicants_page = ApplicantsPage.objects.filter(is_active=True).first()
        
        application_methods = ApplicationMethod.objects.filter(is_active=True).order_by('order')
        enrollment_stages = EnrollmentStage.objects.filter(is_active=True).order_by('order')

        # Данные для фильтров
        program_types = ScheduleProgram.PROGRAM_TYPES
        program_types_list = [pt[0] for pt in program_types]
        program_types_json = json.dumps(program_types_list)

        months = [
            ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
            ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
            ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
            ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')
        ]

        department_filter_maps = {
            'format': defaultdict(set),
            'month_year': defaultdict(set),
            'date': defaultdict(set),
            'program_type': defaultdict(set),
        }
        available_years_set = set()

        programs = ScheduleProgram.objects.filter(
            is_active=True,
            department__isnull=False,
            start_date__isnull=False
        ).select_related('department')

        for prog in programs:
            dept_id = prog.department_id
            if not dept_id:
                continue

            if prog.format:
                department_filter_maps['format'][prog.format].add(dept_id)

            if prog.start_date:
                month_year = prog.start_date.strftime("%Y-%m")
                department_filter_maps['month_year'][month_year].add(dept_id)
                date_str = prog.start_date.strftime("%Y-%m-%d")
                department_filter_maps['date'][date_str].add(dept_id)
                available_years_set.add(prog.start_date.year)

            if prog.program_type:
                department_filter_maps['program_type'][prog.program_type].add(dept_id)

        available_years = sorted(available_years_set, reverse=True)

        filter_maps_json = {
            'format': {k: list(v) for k, v in department_filter_maps['format'].items()},
            'month_year': {k: list(v) for k, v in department_filter_maps['month_year'].items()},
            'date': {k: list(v) for k, v in department_filter_maps['date'].items()},
            'program_type': {k: list(v) for k, v in department_filter_maps['program_type'].items()},
        }

        # تحديد نوع المستخدم
        user_type = ''
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            user_type = request.user.profile.user_type

        context = {
            'documents': documents,
            'featured_schedule_programs': featured_schedule_programs,
            'departments': departments,
            'applicants_page': applicants_page,
            'application_methods': application_methods,
            'enrollment_stages': enrollment_stages,
            'program_types': program_types,
            'program_types_json': program_types_json,
            'months': months,
            'available_years': available_years,
            'filter_maps_json': json.dumps(filter_maps_json),
            'total_departments_count': departments.count(),
            'user_authenticated': request.user.is_authenticated,
            'user_type': user_type,  # تمرير نوع المستخدم إلى القالب
        }
        return render(request, 'applicants/applicants.html', context)
    except Exception as e:
        logger.error(f"Ошибка в applicants_page: {str(e)}\n{traceback.format_exc()}")
        # Возвращаем страницу с ошибкой или редирект на главную
        return render(request, 'applicants/applicants.html', {'error': 'Произошла ошибка при загрузке страницы'})


def foreign_applicants_view(request):
    """
    Страница для иностранных абитуриентов
    """
    try:
        documents = ApplicantDocument.objects.filter(is_active=True)
        featured_schedule_programs = ScheduleProgram.objects.filter(
            is_active=True
        ).order_by('-created_at')[:2]
        departments = Department.objects.filter(is_active=True).order_by('order', 'name')
        applicants_page = ApplicantsPage.objects.filter(is_active=True).first()
        application_methods = ApplicationMethod.objects.filter(is_active=True).order_by('order')
        enrollment_stages = EnrollmentStage.objects.filter(is_active=True).order_by('order')

        program_types = ScheduleProgram.PROGRAM_TYPES
        program_types_list = [pt[0] for pt in program_types]
        program_types_json = json.dumps(program_types_list)

        months = [
            ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
            ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
            ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
            ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')
        ]

        department_filter_maps = {
            'format': defaultdict(set),
            'month_year': defaultdict(set),
            'date': defaultdict(set),
            'program_type': defaultdict(set),
        }
        available_years_set = set()

        programs = ScheduleProgram.objects.filter(
            is_active=True,
            department__isnull=False,
            start_date__isnull=False
        ).select_related('department')

        for prog in programs:
            dept_id = prog.department_id
            if not dept_id:
                continue

            if prog.format:
                department_filter_maps['format'][prog.format].add(dept_id)

            if prog.start_date:
                month_year = prog.start_date.strftime("%Y-%m")
                department_filter_maps['month_year'][month_year].add(dept_id)
                date_str = prog.start_date.strftime("%Y-%m-%d")
                department_filter_maps['date'][date_str].add(dept_id)
                available_years_set.add(prog.start_date.year)

            if prog.program_type:
                department_filter_maps['program_type'][prog.program_type].add(dept_id)

        available_years = sorted(available_years_set, reverse=True)

        filter_maps_json = {
            'format': {k: list(v) for k, v in department_filter_maps['format'].items()},
            'month_year': {k: list(v) for k, v in department_filter_maps['month_year'].items()},
            'date': {k: list(v) for k, v in department_filter_maps['date'].items()},
            'program_type': {k: list(v) for k, v in department_filter_maps['program_type'].items()},
        }

        # تحديد نوع المستخدم
        user_type = ''
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            user_type = request.user.profile.user_type

        context = {
            'documents': documents,
            'featured_schedule_programs': featured_schedule_programs,
            'departments': departments,
            'applicants_page': applicants_page,
            'application_methods': application_methods,
            'enrollment_stages': enrollment_stages,
            'program_types': program_types,
            'program_types_json': program_types_json,
            'months': months,
            'available_years': available_years,
            'filter_maps_json': json.dumps(filter_maps_json),
            'total_departments_count': departments.count(),
            'user_authenticated': request.user.is_authenticated,
            'user_type': user_type,  # تمرير نوع المستخدم إلى القالب
        }
        return render(request, 'applicants/foreign_applicants.html', context)
    except Exception as e:
        logger.error(f"Ошибка в foreign_applicants_view: {str(e)}\n{traceback.format_exc()}")
        return render(request, 'applicants/foreign_applicants.html', {'error': 'Произошла ошибка при загрузке страницы'})


@login_required
@csrf_protect
@require_POST
def submit_application(request):
    try:
        # Rate limiting: не более 5 заявок в час с одного IP
        ip = get_client_ip(request)
        cache_key = f'applicant_submit_{ip}'
        count = cache.get(cache_key, 0)
        if count >= 5:
            logger.warning(f"Превышен лимит заявок для IP {ip}")
            return JsonResponse({
                'success': False,
                'message': 'Превышен лимит заявок (не более 5 в час). Пожалуйста, попробуйте позже.'
            }, status=429)

        # التحقق من نوع المستخدم (يسمح فقط لـ regular, student, company)
        profile = request.user.profile
        allowed_types = ['regular', 'student', 'company']
        if profile.user_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'message': 'Вы не можете подать заявку. Только обычные пользователи, студенты и компании могут подавать заявки.'
            }, status=403)

        # Проверка размера запроса
        if request.content_length and request.content_length > MAX_UPLOAD_SIZE:
            return JsonResponse({
                'success': False,
                'message': 'Слишком большой размер запроса'
            }, status=413)

        # Проверка типа содержимого
        if request.content_type not in ['application/x-www-form-urlencoded', 'multipart/form-data']:
            return JsonResponse({
                'success': False,
                'message': 'Неподдерживаемый тип контента'
            }, status=415)

        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        additional_notes = request.POST.get('additional_notes', '')

        if not all([contact_person, phone, email]):
            return JsonResponse({
                'success': False,
                'message': 'Все обязательные поля должны быть заполнены'
            }, status=400)

        # Проверка email
        if not re.match(EMAIL_PATTERN, email):
            return JsonResponse({
                'success': False,
                'message': 'Некорректный email'
            }, status=400)

        # Проверка телефона
        if not re.match(PHONE_PATTERN, phone):
            return JsonResponse({
                'success': False,
                'message': 'Некорректный номер телефона'
            }, status=400)

        # Создание заявки
        application = ApplicantApplication(
            contact_person=contact_person,
            phone=phone,
            email=email,
            additional_notes=additional_notes
        )

        # Валидация модели
        try:
            application.full_clean()
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            return JsonResponse({
                'success': False,
                'message': 'Ошибка в данных: ' + '; '.join(error_messages)
            }, status=400)

        # Сохранение
        application.save()

        # Увеличиваем счетчик после успешного сохранения
        cache.set(cache_key, count + 1, timeout=3600)

        logger.info(f"Новая заявка отправлена, номер: {application.application_number}")

        return JsonResponse({
            'success': True,
            'application_number': application.application_number,
            'message': 'Заявка успешно отправлена'
        })

    except IntegrityError as e:
        logger.error(f"Ошибка целостности базы данных: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка базы данных. Пожалуйста, попробуйте позже.'
        }, status=500)
    except OperationalError as e:
        logger.error(f"Ошибка подключения к базе данных: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка подключения к базе данных. Пожалуйста, попробуйте позже.'
        }, status=500)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при отправке заявки: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'message': 'Произошла внутренняя ошибка сервера. Пожалуйста, обратитесь к администратору.'
        }, status=500)


@permission_required('applicants.view_applicantapplication', raise_exception=True)
def search_application(request):
    try:
        snils_number = request.GET.get('snils', '')

        # Защита от SQL-инъекций
        if not snils_number or len(snils_number) > 50:
            return JsonResponse({
                'found': False,
                'message': 'Информация по СНИЛС не найдена'
            })

        # Здесь можно добавить логику поиска (если нужно)
        return JsonResponse({
            'found': False,
            'message': 'Информация по СНИЛС не найдена'
        })
    except Exception as e:
        logger.error(f"Ошибка в search_application: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            'found': False,
            'message': 'Произошла ошибка при поиске'
        }, status=500)