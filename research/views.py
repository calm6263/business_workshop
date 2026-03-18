from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta
import json
from .models import (
    Research, ResearchCategory, ResearchHero,
    Conference, ConferenceRegistration,
    YouthCouncilMember, YouthCouncilDepartment
)

def research_list(request):
    categories = ResearchCategory.objects.filter(is_active=True)
    research_list = Research.objects.filter(is_active=True).select_related('category')
    
    research_type = request.GET.get('type')
    if research_type:
        research_list = research_list.filter(research_type=research_type)
    
    category_id = request.GET.get('category')
    if category_id:
        research_list = research_list.filter(category_id=category_id)
    
    period = request.GET.get('period')
    today = timezone.now().date()
    if period == 'month':
        research_list = research_list.filter(publication_date__gte=today - timedelta(days=30))
    elif period == 'quarter':
        research_list = research_list.filter(publication_date__gte=today - timedelta(days=90))
    elif period == 'year':
        research_list = research_list.filter(publication_date__gte=today - timedelta(days=365))
    
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        research_list = research_list.order_by('publication_date')
    elif sort == 'popular':
        research_list = research_list.order_by('-views_count')
    else:
        research_list = research_list.order_by('-publication_date')
    
    research_types = Research.RESEARCH_TYPES

    conference_list = Conference.objects.filter(is_active=True)
    conference_type = request.GET.get('conference_type')
    if conference_type:
        conference_list = conference_list.filter(conference_type=conference_type)
    
    conference_period = request.GET.get('conference_period')
    if conference_period == 'upcoming':
        conference_list = conference_list.filter(start_date__gte=today)
    elif conference_period == 'past':
        conference_list = conference_list.filter(end_date__lt=today)
    elif conference_period == 'this_month':
        conference_list = conference_list.filter(start_date__month=today.month, start_date__year=today.year)
    
    conference_sort = request.GET.get('conference_sort', 'newest')
    if conference_sort == 'oldest':
        conference_list = conference_list.order_by('start_date')
    elif conference_sort == 'popular':
        conference_list = conference_list.order_by('-views_count')
    else:
        conference_list = conference_list.order_by('-start_date')
    
    conference_types = Conference.CONFERENCE_TYPES
    hero = ResearchHero.objects.filter(is_active=True).first()
    current_tab = request.GET.get('tab', 'research')

    # Youth Council members
    youth_council_members = YouthCouncilMember.objects.filter(is_active=True).order_by('order')
    youth_council_departments = YouthCouncilDepartment.objects.filter(
        members__is_active=True,
        is_active=True
    ).distinct().order_by('order', 'name')

    youth_council_by_department = {}
    for dept in youth_council_departments:
        members = youth_council_members.filter(departments=dept)
        if members.exists():
            youth_council_by_department[dept] = members

    context = {
        'research_list': research_list,
        'categories': categories,
        'current_type': research_type,
        'current_category': category_id,
        'current_sort': sort,
        'current_period': period,
        'research_types': research_types,
        'conference_list': conference_list,
        'conference_types': conference_types,
        'current_conference_type': conference_type,
        'current_conference_sort': conference_sort,
        'current_conference_period': conference_period,
        'hero': hero,
        'current_tab': current_tab,
        'youth_council_members': youth_council_members,
        'youth_council_by_department': youth_council_by_department,
        'departments': youth_council_departments,
    }
    return render(request, 'research/research_list.html', context)

def research_detail(request, research_id):
    research = get_object_or_404(Research, id=research_id, is_active=True)
    research.views_count += 1
    research.save()
    
    related_research = Research.objects.filter(
        category=research.category, 
        is_active=True
    ).exclude(id=research.id)[:4]
    
    hero = ResearchHero.objects.filter(is_active=True).first()

    # ===== سياق المؤتمرات =====
    conference_list = Conference.objects.filter(is_active=True)
    conference_type = request.GET.get('conference_type')
    if conference_type:
        conference_list = conference_list.filter(conference_type=conference_type)

    conference_period = request.GET.get('conference_period')
    today = timezone.now().date()
    if conference_period == 'upcoming':
        conference_list = conference_list.filter(start_date__gte=today)
    elif conference_period == 'past':
        conference_list = conference_list.filter(end_date__lt=today)
    elif conference_period == 'this_month':
        conference_list = conference_list.filter(start_date__month=today.month, start_date__year=today.year)

    conference_sort = request.GET.get('conference_sort', 'newest')
    if conference_sort == 'oldest':
        conference_list = conference_list.order_by('start_date')
    elif conference_sort == 'popular':
        conference_list = conference_list.order_by('-views_count')
    else:
        conference_list = conference_list.order_by('-start_date')

    conference_types = Conference.CONFERENCE_TYPES

    # ===== سياق مجلس الشباب =====
    youth_council_members = YouthCouncilMember.objects.filter(is_active=True).order_by('order')
    youth_council_departments = YouthCouncilDepartment.objects.filter(
        members__is_active=True,
        is_active=True
    ).distinct().order_by('order', 'name')

    youth_council_by_department = {}
    for dept in youth_council_departments:
        members = youth_council_members.filter(departments=dept)
        if members.exists():
            youth_council_by_department[dept] = members

    # التبويب النشط من URL
    current_tab = request.GET.get('tab', 'research')

    context = {
        'research': research,
        'related_research': related_research,
        'hero': hero,
        'current_tab': current_tab,
        # للمؤتمرات
        'conference_list': conference_list,
        'conference_types': conference_types,
        'current_conference_type': conference_type,
        'current_conference_sort': conference_sort,
        'current_conference_period': conference_period,
        # لمجلس الشباب
        'youth_council_members': youth_council_members,
        'youth_council_by_department': youth_council_by_department,
        'departments': youth_council_departments,
    }
    return render(request, 'research/research_detail.html', context)

def research_categories(request):
    categories = ResearchCategory.objects.filter(is_active=True)
    research_by_category = []
    
    for category in categories:
        research = Research.objects.filter(category=category, is_active=True)[:6]
        if research:
            research_by_category.append({
                'category': category,
                'research': research
            })
    
    context = {
        'research_by_category': research_by_category,
    }
    return render(request, 'research/categories.html', context)

def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, is_active=True)
    conference.views_count += 1
    conference.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'research/conference_detail_partial.html', {'conference': conference})

    context = {
        'conference': conference,
        'current_tab': 'conferences',
    }
    return render(request, 'research/conference_detail.html', context)

@require_POST
@csrf_exempt
def conference_registration(request, conference_id):
    try:
        data = json.loads(request.body)
        conference = get_object_or_404(Conference, id=conference_id, is_active=True)

        if not conference.can_register:
            return JsonResponse({'success': False, 'error': 'Регистрация на эту конференцию закрыта.'})

        full_name = data.get('full_name')
        phone = data.get('phone')
        email = data.get('email')
        agreement = data.get('agreement')

        if not all([full_name, phone, email, agreement]):
            return JsonResponse({'success': False, 'error': 'Все поля обязательны для заполнения.'})

        registration = ConferenceRegistration(
            conference=conference,
            full_name=full_name,
            phone=phone,
            email=email,
            agreement=agreement
        )
        registration.save()

        return JsonResponse({
            'success': True,
            'message': 'Спасибо за регистрацию! Ваш номер регистрации: ' + registration.registration_number,
            'registration_number': registration.registration_number
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Произошла ошибка. Пожалуйста, попробуйте позже.'})

def youth_council_member_detail(request, pk):
    member = get_object_or_404(YouthCouncilMember, pk=pk, is_active=True)
    context = {'member': member}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'research/youth_council_member_detail_partial.html', context)
    return HttpResponseRedirect(reverse('research:research_list') + '?tab=youth-council')