# templatetags/custom_filters.py
from django import template
from django.db.models import Count, Q
from ..models import *

register = template.Library()

@register.simple_tag
def get_active_slides_count():
    return Slide.objects.filter(is_active=True).count()

@register.simple_tag
def get_active_news_count():
    return News.objects.filter(is_active=True).count()

@register.simple_tag
def get_team_members_count():
    return TeamMember.objects.filter(is_active=True).count()

@register.simple_tag
def get_active_programs_count():
    return ScheduleProgram.objects.filter(is_active=True).count()

@register.simple_tag
def get_customers_count():
    return Customer.objects.count()

@register.simple_tag
def get_pending_applications_count():
    return Application.objects.filter(status='pending').count()

@register.simple_tag
def get_active_employees_count():
    return Employee.objects.filter(is_active=True).count()

@register.simple_tag
def get_active_publications_count():
    return PressPublication.objects.filter(is_active=True).count()

@register.simple_tag
def get_pending_requests_count():
    return PublicationRequest.objects.filter(status='pending').count()