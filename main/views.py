# main/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q, Sum, Avg
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from datetime import datetime, timedelta
from .models import (
    Page, Application, Document, EducationalProgram,
    Slide, License
)

def index(request):
    # استيراد نموذج الأخبار من التطبيق المنفصل
    from news.models import News
    
    slides = Slide.objects.filter(is_active=True).order_by('order')
    # جلب آخر 6 أخبار نشطة للعرض في الصفحة الرئيسية
    latest_news = News.objects.filter(is_active=True).select_related('category').order_by('-publish_date')[:6]
    licenses = License.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'index.html', {
        'slides': slides,
        'news': latest_news,
        'licenses': licenses
    })

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, 'page_detail.html', {'page': page})

@login_required
def admin_dashboard(request):
    stats = {
        'total_pages': Page.objects.filter(is_active=True).count(),
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='pending').count(),
        'total_programs': EducationalProgram.objects.filter(is_active=True).count(),
        'total_slides': Slide.objects.filter(is_active=True).count(),
        'total_licenses': License.objects.filter(is_active=True).count(),
    }
 
    recent_applications = Application.objects.order_by('-created_at')[:5]
    
    # إحصائيات إضافية يمكن إضافتها لاحقاً
    
    context = {
        'stats': stats,
        'recent_applications': recent_applications,
    }
    return render(request, 'admin/dashboard.html', context)

def under_construction(request, page_name=None):
    context = {
        'page_name': page_name or 'Страница'
    }
    return render(request, 'under_construction.html', context)
def custom_400_view(request, exception=None):
    """Страница для ошибки 400 (Bad Request)"""
    return render(request, '400.html', status=400)

def custom_403_view(request, exception=None):
    """Страница для ошибки 403 (Forbidden)"""
    return render(request, '403.html', status=403)

def custom_404_view(request, exception=None):
    """Страница для ошибки 404 (Not Found)"""
    return render(request, '404.html', status=404)

def custom_500_view(request):
    """Страница для ошибки 500 (Internal Server Error)"""
    return render(request, '500.html', status=500)