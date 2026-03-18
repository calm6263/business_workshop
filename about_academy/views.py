from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, IntegerField
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (
    ValuesSection, StatisticsSection, LeaderSpeech, PhotoAlbum,
    MainSlider, DownloadableFile, GalleryImage, Leadership,
    QuoteSection, AcademyTeamMember
)
from departments.models import Department


def about_academy(request):
    main_slider = MainSlider.objects.filter(is_active=True).order_by('order')
    values_section = ValuesSection.objects.filter(is_active=True).first()
    statistics_section = StatisticsSection.objects.filter(is_active=True).first()
    leader_speech = LeaderSpeech.objects.filter(is_active=True).first()
    photo_albums = PhotoAlbum.objects.filter(is_active=True).order_by('order')
    downloadable_files = DownloadableFile.objects.filter(is_active=True).order_by('order')
    quote_section = QuoteSection.objects.filter(is_active=True).first()

    context = {
        'main_slider': main_slider,
        'values_section': values_section,
        'statistics_section': statistics_section,
        'leader_speech': leader_speech,
        'photo_albums': photo_albums,
        'downloadable_files': downloadable_files,
        'quote_section': quote_section,
        'title': 'Об академии'
    }
    return render(request, 'about_academy/about_academy.html', context)


def album_detail(request, album_id):
    album = get_object_or_404(PhotoAlbum, id=album_id, is_active=True)
    images = GalleryImage.objects.filter(album=album, is_active=True).order_by('order')
    return render(request, 'about_academy/album_detail.html', {
        'album': album,
        'images': images,
        'title': f'Альбом: {album.title}'
    })


def leadership_detail(request):
    leader = Leadership.objects.filter(is_active=True).first()
    context = {'leader': leader}
    return render(request, 'about_academy/leadership_detail_partial.html', context)


def team_partial(request):
    members = AcademyTeamMember.objects.filter(is_active=True).select_related('department')

    rank_order = Case(
        When(rank='director', then=1),
        When(rank='deputy_director', then=2),
        When(rank='teacher', then=3),
        When(rank='employee', then=4),
        output_field=IntegerField(),
    )
    members = members.annotate(rank_order=rank_order).order_by('department', 'rank_order', 'order')

    departments = Department.objects.filter(academy_team_members__is_active=True).distinct()
    members_by_department = {}
    for dept in departments:
        dept_members = members.filter(department=dept)
        if dept_members.exists():
            members_by_department[dept] = dept_members

    context = {
        'members_by_department': members_by_department,
        'departments': departments,
    }
    return render(request, 'about_academy/team_partial.html', context)


def academy_team_member_detail(request, pk):
    """AJAX view for team member details"""
    member = get_object_or_404(AcademyTeamMember, pk=pk, is_active=True)
    context = {'member': member}

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'about_academy/team_member_detail_partial.html', context)
    else:
        return HttpResponseRedirect(reverse('about_academy'))