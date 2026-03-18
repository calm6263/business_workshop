# views.py (كامل - بدون تغيير عن النسخة السابقة)
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import JournalIssue, SliderImage, SectionSettings

def journal_home(request):
    search_query = request.GET.get('q', '').strip()
    
    issues = JournalIssue.objects.filter(is_published=True).order_by('-order', '-publication_date')
    
    search_results = None
    if search_query:
        search_results = issues.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        ).order_by('-publication_date')
    
    main_slider_images = SliderImage.objects.filter(is_active=True, carousel_type='main').order_by('order')
    section_settings = SectionSettings.load()
    
    best_issues = JournalIssue.objects.filter(
        is_published=True, 
        show_in_best=True
    ).order_by('best_order', '-publication_date')
    
    new_issues = JournalIssue.objects.filter(
        is_published=True, 
        show_in_new=True
    ).order_by('new_order', '-publication_date')
    
    best_new_ids = list(best_issues.values_list('id', flat=True)) + list(new_issues.values_list('id', flat=True))
    early_issues = issues.exclude(id__in=best_new_ids)[:6]
    
    if not early_issues.exists():
        early_issues = issues[:6]
    
    context = {
        'issues': issues,
        'slider_images': main_slider_images,
        'best_issues': best_issues,
        'new_issues': new_issues,
        'early_issues': early_issues,
        'section_settings': section_settings,
        'search_query': search_query,
        'search_results': search_results,
    }
    return render(request, 'fta_journal/home.html', context)


def journal_detail(request, pk):
    issue = get_object_or_404(JournalIssue, pk=pk, is_published=True)
    pages = issue.pages.all().order_by('order', 'page_number')

    issues = JournalIssue.objects.filter(is_published=True).order_by('-order', '-publication_date')
    best_issues = JournalIssue.objects.filter(is_published=True, show_in_best=True).order_by('best_order', '-publication_date')
    new_issues = JournalIssue.objects.filter(is_published=True, show_in_new=True).order_by('new_order', '-publication_date')
    best_new_ids = list(best_issues.values_list('id', flat=True)) + list(new_issues.values_list('id', flat=True))
    early_issues = issues.exclude(id__in=best_new_ids).exclude(id=issue.id)[:6]
    if not early_issues.exists():
        early_issues = issues.exclude(id=issue.id)[:6]

    context = {
        'issue': issue,
        'pages': pages,
        'early_issues': early_issues,
    }
    return render(request, 'fta_journal/detail.html', context)


def early_issues(request):
    """
    صفحة تعرض جميع الإصدارات المبكرة مع إمكانية التصفية حسب الفترة (شهر/ربع سنة/سنة)
    """
    search_query = request.GET.get('q', '').strip()
    period = request.GET.get('period', '')  # month, quarter, year

    issues = JournalIssue.objects.filter(is_published=True).order_by('-publication_date')
    
    # تطبيق فلتر البحث
    if search_query:
        issues = issues.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # تطبيق فلتر الفترة الزمنية
    if period:
        today = timezone.now().date()
        if period == 'month':
            start_date = today - timedelta(days=30)
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        else:
            start_date = None
        
        if start_date:
            issues = issues.filter(publication_date__gte=start_date)
    
    # تجميع الإصدارات حسب السنة
    years = {}
    for issue in issues:
        year = issue.publication_date.year
        if year not in years:
            years[year] = []
        years[year].append(issue)
    
    # ترتيب السنوات تنازلياً
    sorted_years = sorted(years.items(), reverse=True)
    
    context = {
        'years': sorted_years,
        'search_query': search_query,
    }
    return render(request, 'fta_journal/early_issues.html', context)