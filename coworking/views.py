# views.py
from django.shortcuts import render
from .models import Slider, Tariff

def coworking_home(request):
    slider = Slider.objects.filter(is_active=True).first()
    tariffs = Tariff.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'coworking/home.html', {
        'slider': slider,
        'tariffs': tariffs,
    })