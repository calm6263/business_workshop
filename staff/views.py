from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import TeamMember, TeacherProgram, PageHero
from departments.models import Department

def teachers_and_staff(request):
    teachers = TeamMember.objects.filter(member_type='teacher', is_active=True).order_by('order')
    staff = TeamMember.objects.filter(member_type='staff', is_active=True).order_by('order')
    educational_council = TeamMember.objects.filter(
        member_type='educational_council', 
        is_active=True
    ).order_by('order')
    
    # Получение hero section для страницы
    try:
        page_hero = PageHero.objects.get(page='teachers_staff', is_active=True)
    except PageHero.DoesNotExist:
        page_hero = None
    
    # جلب جميع الأقسام التي لها أعضاء نشطين
    departments = Department.objects.filter(team_members__is_active=True).distinct().order_by('name')
    
    # تنظيم المعلمين حسب الأقسام
    teachers_by_department = {}
    for department in departments:
        teachers_in_dept = teachers.filter(departments=department)
        if teachers_in_dept.exists():
            teachers_by_department[department] = teachers_in_dept
    
    # تنظيم المجلس التعليمي حسب الأقسام
    council_by_department = {}
    for department in departments:
        council_in_dept = educational_council.filter(departments=department)
        if council_in_dept.exists():
            council_by_department[department] = council_in_dept
    
    # تنظيم الموظفين حسب الأقسام
    staff_by_department = {}
    for department in departments:
        staff_in_dept = staff.filter(departments=department)
        if staff_in_dept.exists():
            staff_by_department[department] = staff_in_dept
    
    context = {
        'teachers': teachers,
        'staff': staff,
        'educational_council': educational_council,
        'page_hero': page_hero,
        'departments': departments,
        'teachers_by_department': teachers_by_department,
        'council_by_department': council_by_department,
        'staff_by_department': staff_by_department,
    }
    return render(request, 'staff/teachers_and_staff.html', context)

def team_member_detail(request, pk):
    """عرض تفاصيل عضو الفريق"""
    member = get_object_or_404(TeamMember, pk=pk, is_active=True)
    
    # الحصول على البرامج المرتبطة بهذا العضو (إذا كان مدرساً)
    programs = []
    if member.member_type == 'teacher':
        programs = TeacherProgram.objects.filter(
            teacher=member,
            is_active=True
        ).select_related('program').order_by('order')
    
    context = {
        'member': member,
        'programs': programs,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'staff/team_member_detail_partial.html', context)
    else:
        # إذا كان الطلب غير AJAX، نعيد توجيه إلى صفحة القائمة
        return HttpResponseRedirect(reverse('staff:teachers_and_staff'))