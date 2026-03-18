from django.shortcuts import render

def education_info(request):
    return render(request, 'education_info/education_info.html')