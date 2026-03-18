from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import json
import logging

from .models import News, Category, NewsPageHero, Subscriber
from about_academy.models import PhotoAlbum, GalleryImage
from press_center.models import PressCenterPage
from research.models import Research
from fta_journal.models import JournalIssue, SliderImage, SectionSettings

logger = logging.getLogger(__name__)


def news_list(request):
    # ========== بيانات مشتركة لجميع التبويبات ==========
    categories = Category.objects.all()
    hero_section = NewsPageHero.objects.filter(is_active=True).first()
    current_tab = request.GET.get('tab', 'news')
    journal_page = request.GET.get('journal_page', 'home')

    # بيانات Пресс-центр
    press_page = PressCenterPage.objects.filter(is_active=True).first()
    additional_images = []
    press_hero_image_url = None
    if press_page and press_page.background_image:
        press_hero_image_url = press_page.background_image.url

    research_list = Research.objects.filter(is_active=True).order_by('-publication_date')[:6]

    # ========== معالجة تبويب الأخبار ==========
    if current_tab == 'news':
        news_queryset = News.objects.all()

        q = request.GET.get('q')
        if q:
            news_queryset = news_queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(category__name__icontains=q)
            )

        category_id = request.GET.get('category')
        if category_id:
            news_queryset = news_queryset.filter(category_id=category_id)

        sort_by = request.GET.get('sort', 'newest')
        if sort_by == 'asc':
            news_queryset = news_queryset.order_by('publish_date')
        elif sort_by == 'desc' or sort_by == 'newest':
            news_queryset = news_queryset.order_by('-publish_date')
        elif sort_by == 'popular':
            news_queryset = news_queryset.order_by('-views_count', '-publish_date')

        paginator = Paginator(news_queryset, 9)
        page_number = request.GET.get('page')
        news_page = paginator.get_page(page_number)

        selected_category_name = None
        if category_id:
            try:
                selected_category_name = Category.objects.get(id=category_id).name
            except Category.DoesNotExist:
                pass

        context = {
            'news': news_page,
            'categories': categories,
            'selected_category_name': selected_category_name,
            'hero_section': hero_section,
            'current_tab': current_tab,
            'press_page': press_page,
            'additional_images': additional_images,
            'press_hero_image_url': press_hero_image_url,
            'research_list': research_list,
        }

    # ========== معالجة تبويب Журнал FTA ==========
    elif current_tab == 'journal':
        context = {
            'categories': categories,
            'hero_section': hero_section,
            'current_tab': current_tab,
            'press_page': press_page,
            'additional_images': additional_images,
            'press_hero_image_url': press_hero_image_url,
            'research_list': research_list,
            'journal_page': journal_page,
        }

        if journal_page == 'detail':
            pk = request.GET.get('pk')
            issue = get_object_or_404(JournalIssue, pk=pk, is_published=True)
            pages = issue.pages.all().order_by('order', 'page_number')
            early_issues = JournalIssue.objects.filter(is_published=True).exclude(pk=issue.pk)[:6]

            context.update({
                'journal_issue': issue,
                'journal_pages': pages,
                'journal_early_issues': early_issues,
            })

        elif journal_page == 'early':
            search_query = request.GET.get('q', '').strip()
            period = request.GET.get('period', '')
            issues = JournalIssue.objects.filter(is_published=True).order_by('-publication_date')

            if search_query:
                issues = issues.filter(
                    Q(title__icontains=search_query) | Q(description__icontains=search_query)
                )
            if period:
                today = timezone.now().date()
                delta = {'month': 30, 'quarter': 90, 'year': 365}.get(period)
                if delta:
                    start_date = today - timedelta(days=delta)
                    issues = issues.filter(publication_date__gte=start_date)

            # تجميع الإصدارات حسب السنة
            years = {}
            for issue in issues:
                year = issue.publication_date.year
                years.setdefault(year, []).append(issue)
            sorted_years = sorted(years.items(), reverse=True)

            context.update({
                'years': sorted_years,
                'journal_search_query': search_query,
            })

        else:  # الصفحة الرئيسية للمجلة (home)
            search_query = request.GET.get('q', '').strip()
            main_slider_images = SliderImage.objects.filter(is_active=True, carousel_type='main').order_by('order')
            section_settings = SectionSettings.load()

            best_issues = JournalIssue.objects.filter(is_published=True, show_in_best=True).order_by('best_order')
            new_issues = JournalIssue.objects.filter(is_published=True, show_in_new=True).order_by('new_order')

            best_new_ids = list(best_issues.values_list('id', flat=True)) + list(new_issues.values_list('id', flat=True))

            # جلب الإصدارات المبكرة (غير الموجودة في best و new)
            early_issues = JournalIssue.objects.filter(is_published=True).exclude(id__in=best_new_ids)[:6]

            # إذا لم توجد أي إصدارات مبكرة، نعرض أول 6 إصدارات بشكل افتراضي
            if not early_issues.exists():
                early_issues = JournalIssue.objects.filter(is_published=True)[:6]

            if search_query:
                search_results = JournalIssue.objects.filter(is_published=True).filter(
                    Q(title__icontains=search_query) | Q(description__icontains=search_query)
                ).order_by('-publication_date')
            else:
                search_results = None

            journal_hero_image_url = main_slider_images.first().image.url if main_slider_images.exists() else None

            context.update({
                'journal_slider_images': main_slider_images,
                'journal_section_settings': section_settings,
                'journal_best_issues': best_issues,
                'journal_new_issues': new_issues,
                'journal_early_issues': early_issues,
                'journal_search_query': search_query,
                'journal_search_results': search_results,
                'journal_hero_image_url': journal_hero_image_url,
            })

    # ========== معالجة تبويب Пресс-центр (إذا تم تضمينه في نفس الصفحة) ==========
    else:
        # هذا الفرع لأي تبويب آخر (مثل press) - يمكن إضافته لاحقاً
        context = {
            'categories': categories,
            'hero_section': hero_section,
            'current_tab': current_tab,
            'press_page': press_page,
            'additional_images': additional_images,
            'press_hero_image_url': press_hero_image_url,
            'research_list': research_list,
        }

    return render(request, 'news/news_list.html', context)


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    hero_section = NewsPageHero.objects.filter(is_active=True).first()

    album = PhotoAlbum.objects.filter(is_active=True).first()
    gallery_images = []
    if album:
        gallery_images = GalleryImage.objects.filter(album=album, is_active=True).order_by('order')[:6]

    current_tab = request.GET.get('tab', 'news')

    context = {
        'news_item': news_item,
        'hero_section': hero_section,
        'gallery_images': gallery_images,
        'current_tab': current_tab,
    }
    return render(request, 'news/news_detail.html', context)


@require_POST
def subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        consent = data.get('consent', False)

        if not email:
            return JsonResponse({'success': False, 'error': 'Введите email'})
        if not consent:
            return JsonResponse({'success': False, 'error': 'Необходимо согласие на обработку данных'})

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'consent': consent}
        )
        if not created:
            subscriber.consent = consent
            subscriber.save()

        return JsonResponse({'success': True, 'message': 'Спасибо за подписку!'})
    except Exception as e:
        # تسجيل الخطأ في السجلات بدلاً من عرضه للمستخدم
        logger.error(f"Subscription error for email {data.get('email')}: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'Произошла внутренняя ошибка. Пожалуйста, попробуйте позже.'})