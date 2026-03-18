from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
import json
from collections import defaultdict
from .models import Department, HeroImage

try:
    from schedule.models import ScheduleProgram
    SCHEDULE_AVAILABLE = True
except ImportError:
    ScheduleProgram = None
    SCHEDULE_AVAILABLE = False

def departments_list(request):
    departments = Department.objects.filter(is_active=True).order_by('order', 'name')
    
    try:
        hero_image = HeroImage.objects.get(page='departments_list', is_active=True)
    except HeroImage.DoesNotExist:
        hero_image = None
    
    # ---------- FILTER DATA ----------
    program_types = []
    months = []
    available_years = []
    program_types_json = '[]'
    department_filter_maps = {
        'format': defaultdict(set),
        'month_year': defaultdict(set),
        'date': defaultdict(set),
        'program_type': defaultdict(set),
    }

    if SCHEDULE_AVAILABLE and ScheduleProgram is not None:
        program_types = ScheduleProgram.PROGRAM_TYPES
        program_types_list = [pt[0] for pt in program_types]
        program_types_json = json.dumps(program_types_list)
        
        months = [
            ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
            ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
            ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
            ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')
        ]
        
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
                available_years.append(prog.start_date.year)
            
            if prog.program_type:
                department_filter_maps['program_type'][prog.program_type].add(dept_id)
        
        available_years = sorted(set(available_years), reverse=True)
    
    filter_maps_json = {
        'format': {k: list(v) for k, v in department_filter_maps['format'].items()},
        'month_year': {k: list(v) for k, v in department_filter_maps['month_year'].items()},
        'date': {k: list(v) for k, v in department_filter_maps['date'].items()},
        'program_type': {k: list(v) for k, v in department_filter_maps['program_type'].items()},
    }

    # ---------- ARCHIVE PROGRAMS (for carousel) ----------
    archive_programs = []
    if SCHEDULE_AVAILABLE and ScheduleProgram is not None:
        archive_programs = ScheduleProgram.objects.filter(
            is_active=True,
            enrollment_status='archive'
        ).order_by('-start_date')[:8]

    context = {
        'departments': departments,
        'hero_image': hero_image,
        'program_types': program_types,
        'program_types_json': program_types_json,
        'months': months,
        'available_years': available_years,
        'filter_maps_json': json.dumps(filter_maps_json),
        'total_departments_count': departments.count(),
        'archive_programs': archive_programs,
    }
    return render(request, 'departments/departments_list.html', context)


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk, is_active=True)
    
    try:
        hero_image = HeroImage.objects.get(page='department_detail', is_active=True)
    except HeroImage.DoesNotExist:
        hero_image = None
    
    archive_mode = request.GET.get('archive') == '1'
    
    try:
        from schedule.models import ScheduleProgram
        base_query = ScheduleProgram.objects.filter(
            department=department,
            is_active=True
        )
        if archive_mode:
            department_programs = base_query.filter(enrollment_status='archive')
        else:
            department_programs = base_query.all()
        
        department_programs = department_programs.order_by('start_date', 'order')
        
        program_types = ScheduleProgram.PROGRAM_TYPES
        
        available_years = set()
        for program in department_programs:
            if program.start_date:
                available_years.add(program.start_date.year)
        
        months = [
            (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
            (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
            (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
        ]
    except ImportError:
        department_programs = []
        program_types = []
        available_years = set()
        months = []
    
    related_departments = Department.objects.filter(
        program_type=department.program_type,
        is_active=True
    ).exclude(pk=pk).order_by('order')[:3]
    
    try:
        from schedule.models import ScheduleProgram
        archive_programs = ScheduleProgram.objects.filter(
            is_active=True,
            enrollment_status='archive'
        ).order_by('-start_date')[:8]
    except ImportError:
        archive_programs = []
    
    context = {
        'department': department,
        'department_programs': department_programs,
        'related_departments': related_departments,
        'archive_programs': archive_programs,
        'program_types': program_types,
        'available_years': sorted(list(available_years), reverse=True),
        'months': months,
        'hero_image': hero_image,
        'archive_mode': archive_mode,
    }
    return render(request, 'departments/department_detail.html', context)


def archive_programs_list(request):
    """
    عرض الأقسام التي تحتوي على برامج مؤرشفة (enrollment_status='archive')
    """
    if not SCHEDULE_AVAILABLE or ScheduleProgram is None:
        departments = []
        program_types = []
        months = []
        available_years = []
        total_count = 0
        filter_maps_json = '{}'
        interesting_programs = []
    else:
        archived_programs = ScheduleProgram.objects.filter(
            is_active=True,
            enrollment_status='archive'
        ).select_related('department')

        dept_ids = archived_programs.values_list('department_id', flat=True).distinct()
        departments = Department.objects.filter(id__in=dept_ids, is_active=True) \
                          .annotate(archived_programs_count=Count('programs', filter=Q(programs__enrollment_status='archive', programs__is_active=True))) \
                          .order_by('order', 'name')

        program_types = ScheduleProgram.PROGRAM_TYPES
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

        for prog in archived_programs:
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

        total_count = departments.count()

        interesting_programs = ScheduleProgram.objects.filter(
            is_active=True
        ).exclude(enrollment_status='archive').order_by('-start_date')[:8]

    try:
        hero_image = HeroImage.objects.get(page='departments_list', is_active=True)
    except HeroImage.DoesNotExist:
        hero_image = None

    context = {
        'departments': departments,
        'hero_image': hero_image,
        'program_types': program_types,
        'program_types_json': json.dumps([pt[0] for pt in program_types]),
        'months': months,
        'available_years': available_years,
        'filter_maps_json': json.dumps(filter_maps_json),
        'total_departments_count': total_count,
        'interesting_programs': interesting_programs,
    }
    return render(request, 'departments/archive_programs_list.html', context)