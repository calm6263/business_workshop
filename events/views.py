# events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # سنقوم بإزالة هذا التزيين من الوظائف
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
from .models import Event, InterestingProgram, EventRegistration, NewsletterSubscription, PageSettings, Album, Photo
from django.db.models import Q
from .forms import EventRegistrationForm, NewsletterSubscriptionForm
from accounts.models import UserType  # لاستخدام أنواع المستخدمين

def events_page(request):
    events = Event.objects.filter(is_active=True).order_by('event_type', 'date', 'order')
    
    current_events = events.filter(event_type='current')
    upcoming_events = events.filter(event_type='upcoming')
    past_events = events.filter(event_type='past')
    
    search_query = request.GET.get('q', '').strip()
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(detailed_description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(organizers__icontains=search_query)
        )
        current_events = events.filter(event_type='current')
        upcoming_events = events.filter(event_type='upcoming')
        past_events = events.filter(event_type='past')
    
    page_settings = PageSettings.objects.filter(page_name='events_page').first()
    
    if not page_settings:
        page_settings = PageSettings.objects.create(
            page_name='events_page',
            page_type='events_page',
            hero_title='Мероприятия',
            hero_subtitle='Присоединяйтесь к нашим событиям и развивайтесь вместе с нами',
            is_active=True
        )
    
    context = {
        'current_events': current_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'page_settings': page_settings,
        'search_query': search_query,
        'total_events_count': events.count(),
    }
    return render(request, 'events/events.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)

# تمت إزالة @csrf_exempt لأننا نستخدم CSRF token في الطلبات
def event_detail_api(request, pk):
    """Return event details as JSON for AJAX requests"""
    try:
        event = get_object_or_404(Event, pk=pk, is_active=True)
        
        event_data = {
            'id': event.id,
            'title': event.title,
            'event_type': event.event_type,
            'event_type_display': event.get_event_type_display(),
            'short_description': event.short_description,
            'detailed_description': event.detailed_description,  # هذا المحتوى قد يحتوي على HTML
            'image_url': event.image.url if event.image else '',
            'date': event.date.strftime('%d.%m.%Y') if event.date else '',
            'time': event.time.strftime('%H:%M') if event.time else '',
            'price_display': event.price_display,
            'is_free': event.is_free,
            'location': event.location or 'Уточняется',
            'contact_person': event.contact_person or '',
            'contact_phone': event.contact_phone or '',
            'contact_email': event.contact_email or '',
            'organizers': event.organizers or '',
            'can_register': event.can_register,
            'registration_url': event.registration_url or '',
            'video_url': event.video.url if event.video else '',
            'video_title': event.video_title or 'Как дойти?',
        }
        
        return JsonResponse({
            'success': True,
            'event': event_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_POST
def event_registration(request, pk):
    # التحقق من المصادقة
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})
    
    # التحقق من نوع المستخدم
    profile = request.user.profile
    allowed_types = [UserType.REGULAR, UserType.STUDENT, UserType.COMPANY]
    if profile.user_type not in allowed_types:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав для регистрации на мероприятие'})
    
    try:
        data = json.loads(request.body)
        event = get_object_or_404(Event, pk=pk, is_active=True)
        
        if not event.can_register:
            return JsonResponse({'success': False, 'error': 'Регистрация на это мероприятие закрыта.'})
        
        # استخدام نموذج Django للتحقق
        form = EventRegistrationForm(data)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            return JsonResponse({
                'success': True, 
                'message': 'Спасибо за регистрацию! Ваш номер регистрации: ' + registration.registration_number,
                'registration_number': registration.registration_number
            })
        else:
            # تجميع أخطاء النموذج
            errors = {}
            for field, err_list in form.errors.items():
                errors[field] = err_list[0]
            return JsonResponse({'success': False, 'error': errors}, status=400)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Произошла ошибка. Пожалуйста, попробуйте позже.'})

def interesting_program_detail(request, slug):
    program = get_object_or_404(InterestingProgram, slug=slug, is_active=True)
    
    related_programs = InterestingProgram.objects.filter(
        is_active=True
    ).exclude(slug=slug).order_by('order')[:3]
    
    context = {
        'program': program,
        'related_programs': related_programs,
    }
    return render(request, 'events/interesting_program_detail.html', context)

@require_POST
def newsletter_subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        agreement = data.get('agreement')

        # استخدام نموذج Django
        form = NewsletterSubscriptionForm(data)
        if form.is_valid():
            email = form.cleaned_data['email']
            agreement = form.cleaned_data['agreement']

            if NewsletterSubscription.objects.filter(email=email).exists():
                subscription = NewsletterSubscription.objects.get(email=email)
                if subscription.is_active:
                    return JsonResponse({'success': False, 'error': 'Этот адрес электронной почты уже подписан.'})
                else:
                    subscription.is_active = True
                    subscription.agreement = agreement
                    subscription.save()
            else:
                subscription = NewsletterSubscription(
                    email=email,
                    agreement=agreement
                )
                subscription.save()

            return JsonResponse({
                'success': True, 
                'message': 'Спасибо за подписку на нашу рассылку! Вы будете получать последние новости о наших мероприятиях.'
            })
        else:
            errors = {}
            for field, err_list in form.errors.items():
                errors[field] = err_list[0]
            return JsonResponse({'success': False, 'error': errors}, status=400)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Произошла ошибка. Пожалуйста, попробуйте позже.'})

def search_events_api(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        event_type = request.GET.get('type', 'all')
        
        events = Event.objects.filter(is_active=True)
        
        if event_type != 'all':
            events = events.filter(event_type=event_type)
        
        if query:
            events = events.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(detailed_description__icontains=query) |
                Q(location__icontains=query) |
                Q(organizers__icontains=query)
            )
        
        events = events.order_by('event_type', 'date', 'order')
        
        results = []
        for event in events:
            results.append({
                'id': event.id,
                'title': event.title,
                'short_description': event.short_description,
                'event_type': event.event_type,
                'event_type_display': event.get_event_type_display(),
                'date': event.date.strftime('%d.%m.%Y'),
                'time': event.time.strftime('%H:%M') if event.time else None,
                'price_display': event.price_display,
                'location': event.location,
                'image_url': event.image.url if event.image else '',
                'detail_url': event.get_absolute_url(),
                'can_register': event.can_register,
            })
        
        return JsonResponse({
            'success': True,
            'query': query,
            'event_type': event_type,
            'count': len(results),
            'results': results
        })
    
    return JsonResponse({'success': False, 'error': 'Метод не разрешен'}, status=405)

def gallery(request):
    albums = Album.objects.filter(is_active=True).order_by('-event_date', 'order')
    
    search_query = request.GET.get('q', '').strip()
    if search_query:
        albums = albums.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    page_settings = PageSettings.objects.filter(page_name='gallery_page').first()
    
    if not page_settings:
        page_settings = PageSettings.objects.create(
            page_name='gallery_page',
            page_type='gallery_page',
            hero_title='Фотогалерея',
            hero_subtitle='Воспоминания о наших мероприятиях в фотографиях',
            is_active=True
        )
    
    context = {
        'albums': albums,
        'page_settings': page_settings,
    }
    return render(request, 'events/gallery.html', context)

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, is_active=True)
    photos = album.photos.filter(is_active=True).order_by('order', 'created_at')
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'events/album_detail.html', context)