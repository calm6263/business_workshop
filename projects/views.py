from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, ProjectCategory, ProjectSlide, ProjectPartner, ContactRequest, ProjectProposal, ProjectGallery, ProjectJoinRequest
from datetime import timedelta
from django.utils import timezone
import re

def projects_list(request):
    categories = ProjectCategory.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True).select_related('category')
    slides = ProjectSlide.objects.filter(is_active=True).order_by('order')
    
    # الفلتر الأول: البحث
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # الفلتر الثاني: التصنيف
    category_id = request.GET.get('category', '')
    if category_id:
        projects = projects.filter(category_id=category_id)
    
    # الحصول على اسم التصنيف الحالي إذا كان موجودًا
    current_category_name = ""
    if category_id:
        try:
            current_category = categories.get(id=category_id)
            current_category_name = current_category.name
        except ProjectCategory.DoesNotExist:
            current_category_name = ""
    
    context = {
        'categories': categories,
        'projects': projects,
        'current_category': category_id,
        'current_category_name': current_category_name,
        'search_query': search_query,
        'slides': slides,
    }
    return render(request, 'projects/projects_list.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_active=True)
    members = project.projectmember_set.filter(is_active=True)
    partners = project.projectpartner_set.filter(is_active=True).order_by('order')
    related_projects = Project.objects.filter(
        category=project.category, 
        is_active=True
    ).exclude(id=project.id)[:3]
    
    gallery_images = ProjectGallery.objects.filter(
        is_active=True
    ).filter(
        Q(project=project) | Q(project__isnull=True)
    ).order_by('order')[:10]
    
    context = {
        'project': project,
        'members': members,
        'partners': partners,
        'related_projects': related_projects,
        'gallery_images': gallery_images,
    }
    return render(request, 'projects/project_detail.html', context)

def contact_request(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id, is_active=True)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        
        if not name or not email or not message_text:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return redirect('projects:project_detail', project_id=project_id)
        
        if not request.POST.get('robotCheck'):
            messages.error(request, 'Пожалуйста, подтвердите, что вы не робот.')
            return redirect('projects:project_detail', project_id=project_id)
        
        ContactRequest.objects.create(
            project=project,
            name=name,
            email=email,
            message=message_text
        )
        
        messages.success(request, 'Ваш запрос успешно отправлен. Мы свяжемся с вами в ближайшее время.')
        return redirect('projects:project_detail', project_id=project_id)
    
    return redirect('projects:project_detail', project_id=project_id)

def submit_project_proposal(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            person_type = request.POST.get('person_type', 'individual')
            
            if person_type == 'individual':
                # جمع بيانات الشخص الطبيعي
                full_name = request.POST.get('full_name_individual', '').strip()
                phone = request.POST.get('phone', '').strip()
                email = request.POST.get('email', '').strip()
                address = request.POST.get('address', '').strip()
                comments = request.POST.get('comments_individual', '').strip()
                
                # التحقق من صحة البريد الإلكتروني
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный email адрес.'
                    })
                
                # التحقق من صحة رقم الهاتف (شكل +7XXXXXXXXXX)
                phone_pattern = r'^\+7\d{10}$'
                if not re.match(phone_pattern, phone):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX.'
                    })
                
                # التحقق من عدم تكرار الطلب (نفس البريد الإلكتروني أو رقم الهاتف خلال 24 ساعة)
                time_threshold = timezone.now() - timedelta(hours=24)
                
                # البحث عن طلبات سابقة بنفس البريد أو الهاتف خلال 24 ساعة
                duplicate_proposals = ProjectProposal.objects.filter(
                    Q(email=email) | Q(phone=phone),
                    created_at__gte=time_threshold
                ).exists()
                
                if duplicate_proposals:
                    return JsonResponse({
                        'success': False,
                        'message': 'Вы уже отправили предложение с этим email или телефоном в течение последних 24 часов. Пожалуйста, подождите.'
                    })
                
                # إنشاء عنوان ووصف للمقترح
                title = 'Предложение проекта от физического лица'
                description = f"""ФИО: {full_name}
Телефон: {phone}
Email: {email}
Адрес: {address}
Комментарии: {comments if comments else 'Не указано'}"""
                
                # حفظ المقترح
                proposal = ProjectProposal.objects.create(
                    title=title,
                    description=description,
                    full_name=full_name,
                    email=email,
                    phone=phone
                )
                
            else:  # person_type == 'legal'
                # جمع بيانات الشخص الاعتباري
                full_name = request.POST.get('full_name', '').strip()
                phone = request.POST.get('phone_legal', '').strip()
                email = request.POST.get('email_legal', '').strip()
                company_name = request.POST.get('company_name', '').strip()
                inn = request.POST.get('inn', '').strip()
                kpp = request.POST.get('kpp', '').strip()
                legal_address = request.POST.get('legal_address', '').strip()
                comments = request.POST.get('comments', '').strip()
                
                # التحقق من صحة البريد الإلكتروني
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный email адрес.'
                    })
                
                # التحقق من صحة رقم الهاتف
                phone_pattern = r'^\+7\d{10}$'
                if not re.match(phone_pattern, phone):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX.'
                    })
                
                # التحقق من صحة INN (10 أو 12 رقمًا)
                inn_pattern = r'^\d{10}|\d{12}$'
                if not re.match(inn_pattern, inn):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный ИНН (10 или 12 цифр).'
                    })
                
                # التحقق من صحة KPP (9 أرقام، اختياري)
                if kpp and not re.match(r'^\d{9}$', kpp):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный КПП (9 цифр).'
                    })
                
                # التحقق من عدم تكرار الطلب (نفس البريد، الهاتف، أو INN خلال 24 ساعة)
                time_threshold = timezone.now() - timedelta(hours=24)
                
                # البحث عن طلبات سابقة بنفس البيانات خلال 24 ساعة
                duplicate_proposals = ProjectProposal.objects.filter(
                    Q(email=email) | Q(phone=phone) | Q(description__icontains=f"ИНН: {inn}"),
                    created_at__gte=time_threshold
                ).exists()
                
                if duplicate_proposals:
                    return JsonResponse({
                        'success': False,
                        'message': 'Вы уже отправили предложение с этими данными (email, телефон или ИНН) в течение последних 24 часов. Пожалуйста, подождите.'
                    })
                
                # إنشاء عنوان ووصف للمقترح
                title = 'Предложение проекта от юридического лица'
                description = f"""Ответственное лицо: {full_name}
Телефон: {phone}
Email: {email}
Компания: {company_name}
ИНН: {inn}
КПП: {kpp if kpp else 'Не указано'}
Юридический адрес: {legal_address}
Комментарии: {comments if comments else 'Не указано'}"""
                
                # حفظ المقترح
                proposal = ProjectProposal.objects.create(
                    title=title,
                    description=description,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    organization=company_name
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Ваше предложение успешно отправлено! Мы свяжемся с вами в ближайшее время.',
                'proposal_id': proposal.unique_id
            })
            
        except Exception as e:
            print(f"Error submitting proposal: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при отправке предложения. Пожалуйста, попробуйте еще раз.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Неверный метод запроса.'
    })

def submit_join_request(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            project_id = request.POST.get('project_id')
            project = get_object_or_404(Project, id=project_id, is_active=True)
            person_type = request.POST.get('person_type', 'individual')
            
            # التحقق من عدم تكرار الطلب (نفس البريد الإلكتروني لنفس المشروع خلال 24 ساعة)
            time_threshold = timezone.now() - timedelta(hours=24)
            
            if person_type == 'individual':
                email = request.POST.get('email', '').strip()
                duplicate_requests = ProjectJoinRequest.objects.filter(
                    project=project,
                    email_individual=email,
                    created_at__gte=time_threshold
                ).exists()
            else:
                email = request.POST.get('email_legal', '').strip()
                duplicate_requests = ProjectJoinRequest.objects.filter(
                    project=project,
                    email_legal=email,
                    created_at__gte=time_threshold
                ).exists()
            
            if duplicate_requests:
                return JsonResponse({
                    'success': False,
                    'message': 'Вы уже отправили заявку на вступление в этот проект с этим email в течение последних 24 часов. Пожалуйста, подождите.'
                })
            
            # التحقق من صحة البيانات
            if person_type == 'individual':
                # التحقق من البريد الإلكتروني
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный email адрес.'
                    })
                
                # التحقق من رقم الهاتف
                phone = request.POST.get('phone', '').strip()
                phone_pattern = r'^\+7\d{10}$'
                if not re.match(phone_pattern, phone):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX.'
                    })
            else:
                # التحقق من البريد الإلكتروني للشخص الاعتباري
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный email адрес.'
                    })
                
                # التحقق من رقم الهاتف للشخص الاعتباري
                phone = request.POST.get('phone_legal', '').strip()
                phone_pattern = r'^\+7\d{10}$'
                if not re.match(phone_pattern, phone):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX.'
                    })
                
                # التحقق من INN
                inn = request.POST.get('inn', '').strip()
                inn_pattern = r'^\d{10}|\d{12}$'
                if not re.match(inn_pattern, inn):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный ИНН (10 или 12 цифр).'
                    })
                
                # التحقق من KPP (اختياري)
                kpp = request.POST.get('kpp', '').strip()
                if kpp and not re.match(r'^\d{9}$', kpp):
                    return JsonResponse({
                        'success': False,
                        'message': 'Пожалуйста, введите корректный КПП (9 цифр).'
                    })
            
            # إنشاء طلب الانضمام
            join_request = ProjectJoinRequest.objects.create(
                project=project,
                person_type=person_type
            )
            
            # تعيين البيانات بناءً على نوع الشخص
            if person_type == 'individual':
                join_request.full_name_individual = request.POST.get('full_name_individual', '').strip()
                join_request.phone_individual = request.POST.get('phone', '').strip()
                join_request.email_individual = email
                join_request.address_individual = request.POST.get('address', '').strip()
                join_request.comments_individual = request.POST.get('comments_individual', '').strip()
            else:
                join_request.full_name_legal = request.POST.get('full_name', '').strip()
                join_request.phone_legal = phone
                join_request.email_legal = email
                join_request.company_name = request.POST.get('company_name', '').strip()
                join_request.inn = inn
                join_request.kpp = kpp
                join_request.legal_address = request.POST.get('legal_address', '').strip()
                join_request.comments_legal = request.POST.get('comments', '').strip()
            
            join_request.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Ваша заявка на вступление в проект успешно отправлена! Мы свяжемся с вами в ближайшее время.',
                'request_id': join_request.unique_id
            })
            
        except Exception as e:
            print(f"Error submitting join request: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Произошла ошибка при отправке заявки. Пожалуйста, попробуйте еще раз.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Неверный метод запроса.'
    })