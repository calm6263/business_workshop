# schedule/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
import json
from collections import defaultdict
from datetime import datetime, date

from .models import ScheduleProgram, CurriculumModule, CurriculumDocument, ProgramApplication, ScheduleSliderImage, CalendarSliderImage
from staff.models import TeacherProgram
from departments.models import Department

from .pdf_utils import download_calendar_pdf, download_calendar_pdf_simple

def schedule_page(request):
    try:
        # جلب صور السلايدر النشطة
        slider_images = ScheduleSliderImage.objects.filter(is_active=True).order_by('order')
        
        # ===== دعم التصفية عبر GET =====
        program_type_filter = request.GET.get('type')
        format_filter = request.GET.get('format')
        
        schedules = ScheduleProgram.objects.filter(
            is_active=True, 
            start_date__isnull=False
        )
        
        if program_type_filter and program_type_filter in dict(ScheduleProgram.PROGRAM_TYPES).keys():
            schedules = schedules.filter(program_type=program_type_filter)
        
        if format_filter and format_filter in dict(ScheduleProgram.FORMAT_CHOICES).keys():
            schedules = schedules.filter(format=format_filter)
        
        schedules = schedules.order_by('start_date', 'order')
        
        # ===== تجميع البيانات حسب الشهر (جميع الأشهر) =====
        monthly_schedules = defaultdict(list)
        for schedule in schedules:
            if schedule.start_date:
                month_year = schedule.start_date.strftime("%Y-%m")
                monthly_schedules[month_year].append(schedule)
        
        monthly_data = []
        for month_year, programs in monthly_schedules.items():
            try:
                dt = datetime.strptime(month_year, "%Y-%m")
                month_names_ru = {
                    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
                    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
                }
                month_name = month_names_ru.get(dt.month, dt.strftime("%B"))
                monthly_data.append({
                    'month_year': month_year,
                    'month_name': month_name,
                    'year': dt.year,
                    'programs': programs,
                    'programs_count': len(programs)
                })
            except ValueError as e:
                print(f"Ошибка обработки даты {month_year}: {e}")
                continue
        
        monthly_data.sort(key=lambda x: x['month_year'])
        
        # ===== تحديد الشهرين الأقرب للتاريخ الحالي =====
        today = date.today()
        expanded_months = []
        for month in monthly_data:
            # هل يحتوي الشهر على برنامج يبدأ اليوم أو بعده؟
            if any(p.start_date >= today for p in month['programs']):
                expanded_months.append(month['month_year'])
                if len(expanded_months) == 2:
                    break
        
        # ===== إعداد باقي البيانات =====
        available_years = sorted(set(
            schedule.start_date.year for schedule in schedules 
            if schedule.start_date
        ), reverse=True)
        
        if not available_years:
            available_years = [date.today().year]
        
        program_types = ScheduleProgram.PROGRAM_TYPES
        
        months = [
            ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
            ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
            ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
            ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')
        ]
        
        total_programs_count = sum(month['programs_count'] for month in monthly_data)
        
        # الحصول على البرامج الأرشيفية
        archive_programs = ScheduleProgram.objects.filter(
            is_active=True,
            enrollment_status='archive'
        ).order_by('-start_date')[:8]
        
        # تحضير بيانات JSON لأنواع البرامج للاستخدام في JavaScript
        program_types_list = [pt[0] for pt in program_types]
        
        context = {
            'slider_images': slider_images,
            'monthly_data': monthly_data,                # جميع الأشهر
            'expanded_months': expanded_months,          # أسماء الأشهر المفتوحة (شهرين فقط)
            'available_years': available_years,
            'program_types': program_types,
            'months': months,
            'total_programs_count': total_programs_count,
            'archive_programs': archive_programs,
            'program_types_json': json.dumps(program_types_list),
        }
        return render(request, 'schedule/schedule.html', context)
        
    except Exception as e:
        print(f"Ошибка в представлении расписания: {e}")
        context = {
            'slider_images': [],
            'monthly_data': [],
            'expanded_months': [],
            'available_years': [date.today().year],
            'program_types': ScheduleProgram.PROGRAM_TYPES,
            'months': [
                ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
                ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
                ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
                ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')
            ],
            'total_programs_count': 0,
            'archive_programs': [],
            'program_types_json': json.dumps([]),
            'error': str(e)
        }
        return render(request, 'schedule/schedule.html', context)


def program_detail(request, slug):
    try:
        program = get_object_or_404(ScheduleProgram, slug=slug, is_active=True)
        
        # Получить преподавателей, связанных с программой
        teachers = TeacherProgram.objects.filter(program=program, is_active=True).select_related('teacher')
        
        # Получить отделение, связанное с программой
        department = program.department
        
        # Получить модули учебной программы
        curriculum_modules = program.curriculum_modules.all().order_by('order')
        
        # Получить документы программы обучения (учебные материалы)
        curriculum_documents = program.curriculum_documents.filter(is_active=True).order_by('order')
        
        same_month_programs = ScheduleProgram.objects.filter(
            start_date__year=program.start_date.year,
            start_date__month=program.start_date.month,
            is_active=True
        ).exclude(id=program.id).order_by('start_date')[:3]

        # Определить, пришел ли пользователь со страницы отделения
        from_department = request.GET.get('from') == 'department'

        # الإضافات الجديدة
        departments = []
        if Department is not None:
            departments = Department.objects.all()
        
        all_programs = ScheduleProgram.objects.filter(is_active=True).order_by('title')
        
        other_programs = ScheduleProgram.objects.filter(
            is_active=True,
            program_type=program.program_type
        ).exclude(id=program.id).order_by('start_date')[:8]

        context = {
            'program': program,
            'same_month_programs': same_month_programs,
            'teachers': teachers,
            'department': department,
            'curriculum_modules': curriculum_modules,
            'curriculum_documents': curriculum_documents,
            'from_department': from_department,
            'departments': departments,
            'all_programs': all_programs,
            'other_programs': other_programs,
        }
        return render(request, 'schedule/program_detail.html', context)
    except Exception as e:
        print(f"Ошибка в представлении деталей программы: {e}")
        from django.shortcuts import redirect
        return redirect('schedule:schedule_page')


def submit_application(request, slug):
    if request.method == 'POST':
        try:
            program = get_object_or_404(ScheduleProgram, slug=slug, is_active=True)
            
            # Создать новую заявку
            application = ProgramApplication(
                program=program,
                contact_name=request.POST.get('contactName'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                additional_info=request.POST.get('additionalInfo', ''),
                agreement=bool(request.POST.get('agreement'))
            )
            application.save()
            
            return JsonResponse({
                'success': True,
                'application_number': application.application_number,
                'message': f'Заявка успешно отправлена! Ваш номер заявки: {application.application_number}'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Произошла ошибка: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Неверный метод запроса'
    })


def calendar_view(request):
    """صفحة التقويم السنوي للبرامج"""
    try:
        # جلب صور السلايدر النشطة
        slider_images = CalendarSliderImage.objects.filter(is_active=True).order_by('order')
        
        # جلب البرامج النشطة
        programs = ScheduleProgram.objects.filter(
            is_active=True,
            start_date__isnull=False
        ).order_by('start_date')
        
        # تحضير البيانات للتقويم
        calendar_data = {}
        for program in programs:
            if program.start_date:
                date_str = program.start_date.strftime("%Y-%m-%d")
                if date_str not in calendar_data:
                    calendar_data[date_str] = []
                
                calendar_data[date_str].append({
                    'title': program.title,
                    'program_type': program.program_type,
                    'program_type_display': program.get_program_type_display(),
                    'slug': program.slug,
                })
        
        context = {
            'slider_images': slider_images,
            'calendar_data': json.dumps(calendar_data),
        }
        return render(request, 'schedule/calendar.html', context)
        
    except Exception as e:
        print(f"Ошибка в представлении календаря: {e}")
        context = {
            'slider_images': [],
            'calendar_data': json.dumps({}),
            'error': str(e)
        }
        return render(request, 'schedule/calendar.html', context)