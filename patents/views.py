from django.shortcuts import render
from .models import PatentImage

def patents_list(request):
    """Страница со списком патентов - отображает изображения из базы данных"""
    images = PatentImage.objects.filter(is_active=True).order_by('order')
    return render(request, 'patents/patents_list.html', {'patent_images': images})