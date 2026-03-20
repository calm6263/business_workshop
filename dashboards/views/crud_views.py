# dashboards/views/crud_views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from PIL import Image
from about_academy.models import (
    MainSlider, ValuesSection, StatisticsSection, LeaderSpeech,
    PhotoAlbum, GalleryImage, DownloadableFile, QuoteSection,
    Leadership, AcademyTeamMember, LeaderSpeechVideo
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView
from ..forms import GalleryImageFormSet

# ---------------------- MainSlider ----------------------
class MainSliderListView(BaseAdminListView):
    model = MainSlider
    template_name = 'dashboards/crud/main_slider_list.html'
    context_object_name = 'items'

class MainSliderCreateView(BaseAdminCreateView):
    model = MainSlider
    fields = ['title', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/main_slider_form.html'
    success_url = reverse_lazy('dashboards:main_slider_list')
    success_message = "Слайд успешно добавлен"

class MainSliderUpdateView(BaseAdminUpdateView):
    model = MainSlider
    fields = ['title', 'description', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/main_slider_form.html'
    success_url = reverse_lazy('dashboards:main_slider_list')
    success_message = "Слайд успешно обновлен"

class MainSliderDeleteView(BaseAdminDeleteView):
    model = MainSlider
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:main_slider_list')
    success_message = "Слайд удален"

# ---------------------- ValuesSection ----------------------
class ValuesSectionListView(BaseAdminListView):
    model = ValuesSection
    template_name = 'dashboards/crud/values_list.html'
    context_object_name = 'items'

class ValuesSectionCreateView(BaseAdminCreateView):
    model = ValuesSection
    fields = '__all__'
    template_name = 'dashboards/crud/values_form.html'
    success_url = reverse_lazy('dashboards:values_list')
    success_message = "Раздел ценностей добавлен"

class ValuesSectionUpdateView(BaseAdminUpdateView):
    model = ValuesSection
    fields = '__all__'
    template_name = 'dashboards/crud/values_form.html'
    success_url = reverse_lazy('dashboards:values_list')
    success_message = "Раздел ценностей обновлен"

class ValuesSectionDeleteView(BaseAdminDeleteView):
    model = ValuesSection
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:values_list')
    success_message = "Раздел ценностей удален"

# ---------------------- StatisticsSection ----------------------
class StatisticsSectionListView(BaseAdminListView):
    model = StatisticsSection
    template_name = 'dashboards/crud/statistics_list.html'
    context_object_name = 'items'

class StatisticsSectionCreateView(BaseAdminCreateView):
    model = StatisticsSection
    fields = '__all__'
    template_name = 'dashboards/crud/statistics_form.html'
    success_url = reverse_lazy('dashboards:statistics_list')
    success_message = "Статистика добавлена"

class StatisticsSectionUpdateView(BaseAdminUpdateView):
    model = StatisticsSection
    fields = '__all__'
    template_name = 'dashboards/crud/statistics_form.html'
    success_url = reverse_lazy('dashboards:statistics_list')
    success_message = "Статистика обновлена"

class StatisticsSectionDeleteView(BaseAdminDeleteView):
    model = StatisticsSection
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:statistics_list')
    success_message = "Статистика удалена"

# ---------------------- LeaderSpeech ----------------------
class LeaderSpeechListView(BaseAdminListView):
    model = LeaderSpeech
    template_name = 'dashboards/crud/leaderspeech_list.html'
    context_object_name = 'items'

class LeaderSpeechCreateView(BaseAdminCreateView):
    model = LeaderSpeech
    fields = ['title', 'is_active', 'order']
    template_name = 'dashboards/crud/leaderspeech_form.html'
    success_url = reverse_lazy('dashboards:leaderspeech_list')
    success_message = "Речь руководителя добавлена"

class LeaderSpeechUpdateView(BaseAdminUpdateView):
    model = LeaderSpeech
    fields = ['title', 'is_active', 'order']
    template_name = 'dashboards/crud/leaderspeech_form.html'
    success_url = reverse_lazy('dashboards:leaderspeech_list')
    success_message = "Речь руководителя обновлена"

class LeaderSpeechDeleteView(BaseAdminDeleteView):
    model = LeaderSpeech
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:leaderspeech_list')
    success_message = "Речь руководителя удалена"

# ========== LeaderSpeechVideo ==========
class LeaderSpeechVideoListView(BaseAdminListView):
    model = LeaderSpeechVideo
    template_name = 'dashboards/crud/leaderspeechvideo_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        qs = super().get_queryset()
        leader_id = self.request.GET.get('leader')
        if leader_id:
            qs = qs.filter(leader_speech_id=leader_id)
        return qs.select_related('leader_speech')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leader_id = self.request.GET.get('leader')
        if leader_id:
            ctx['leader'] = get_object_or_404(LeaderSpeech, pk=leader_id)
        return ctx


class LeaderSpeechVideoCreateView(BaseAdminCreateView):
    model = LeaderSpeechVideo
    fields = ['leader_speech', 'title', 'video_url', 'video_file', 'thumbnail', 'order', 'is_active']
    template_name = 'dashboards/crud/leaderspeechvideo_form.html'
    success_message = "Видео успешно добавлено"

    def get_success_url(self):
        leader_id = self.object.leader_speech_id
        return reverse_lazy('dashboards:leaderspeechvideo_list') + f'?leader={leader_id}'


class LeaderSpeechVideoUpdateView(BaseAdminUpdateView):
    model = LeaderSpeechVideo
    fields = ['leader_speech', 'title', 'video_url', 'video_file', 'thumbnail', 'order', 'is_active']
    template_name = 'dashboards/crud/leaderspeechvideo_form.html'
    success_message = "Видео успешно обновлено"

    def get_success_url(self):
        leader_id = self.object.leader_speech_id
        return reverse_lazy('dashboards:leaderspeechvideo_list') + f'?leader={leader_id}'


class LeaderSpeechVideoDeleteView(BaseAdminDeleteView):
    model = LeaderSpeechVideo
    template_name = 'dashboards/crud/confirm_delete.html'
    success_message = "Видео удалено"

    def get_success_url(self):
        leader_id = self.object.leader_speech_id
        return reverse_lazy('dashboards:leaderspeechvideo_list') + f'?leader={leader_id}'

# ---------------------- PhotoAlbum ----------------------
class PhotoAlbumListView(BaseAdminListView):
    model = PhotoAlbum
    template_name = 'dashboards/crud/photoalbum_list.html'
    context_object_name = 'items'

class PhotoAlbumCreateView(BaseAdminCreateView):
    model = PhotoAlbum
    fields = ['title', 'cover_image', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/photoalbum_form_with_images.html'
    success_url = reverse_lazy('dashboards:photoalbum_list')
    success_message = "Альбом добавлен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = GalleryImageFormSet(self.request.POST, self.request.FILES, instance=None)
        else:
            context['formset'] = GalleryImageFormSet(instance=None)
        return context

    def form_valid(self, form):
        self.object = form.save()
        # حفظ الصور الجديدة المرفوعة متعددة
        files = self.request.FILES.getlist('image')
        saved_count = 0
        for file in files:
            try:
                img = Image.open(file)
                img.verify()
                file.seek(0)
                GalleryImage.objects.create(
                    album=self.object,
                    image=file,
                    order=0,
                    is_active=True
                )
                saved_count += 1
            except Exception:
                pass
        if saved_count:
            messages.success(self.request, f"Добавлено {saved_count} фото.")
        return super().form_valid(form)

class PhotoAlbumUpdateView(BaseAdminUpdateView):
    model = PhotoAlbum
    fields = ['title', 'cover_image', 'description', 'order', 'is_active']
    template_name = 'dashboards/crud/photoalbum_form_with_images.html'
    success_url = reverse_lazy('dashboards:photoalbum_list')
    success_message = "Альбом обновлен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = GalleryImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = GalleryImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save()
        # حفظ الصور الجديدة المرفوعة متعددة
        files = self.request.FILES.getlist('image')
        saved_count = 0
        for file in files:
            try:
                img = Image.open(file)
                img.verify()
                file.seek(0)
                GalleryImage.objects.create(
                    album=self.object,
                    image=file,
                    order=0,
                    is_active=True
                )
                saved_count += 1
            except Exception:
                pass
        if saved_count:
            messages.success(self.request, f"Добавлено {saved_count} новых фото.")

        # معالجة التعديلات على الصور الموجودة (order, is_active, حذف)
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)

class PhotoAlbumDeleteView(BaseAdminDeleteView):
    model = PhotoAlbum
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:photoalbum_list')
    success_message = "Альбом удален"

# ---------------------- GalleryImage ----------------------
class GalleryImageListView(BaseAdminListView):
    model = GalleryImage
    template_name = 'dashboards/crud/galleryimage_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        qs = super().get_queryset()
        album_id = self.request.GET.get('album')
        if album_id:
            qs = qs.filter(album_id=album_id)
        return qs.select_related('album')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_id = self.request.GET.get('album')
        if album_id:
            context['album'] = get_object_or_404(PhotoAlbum, pk=album_id)
        return context

class GalleryImageCreateView(BaseAdminCreateView):
    model = GalleryImage
    fields = ['album', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/galleryimage_form.html'
    success_message = "Изображение добавлено"

    def get_success_url(self):
        album_id = self.object.album_id
        return reverse_lazy('dashboards:galleryimage_list') + f'?album={album_id}'

class GalleryImageUpdateView(BaseAdminUpdateView):
    model = GalleryImage
    fields = ['album', 'image', 'order', 'is_active']
    template_name = 'dashboards/crud/galleryimage_form.html'
    success_message = "Изображение обновлено"

    def get_success_url(self):
        album_id = self.object.album_id
        return reverse_lazy('dashboards:galleryimage_list') + f'?album={album_id}'

class GalleryImageDeleteView(BaseAdminDeleteView):
    model = GalleryImage
    template_name = 'dashboards/crud/confirm_delete.html'
    success_message = "Изображение удалено"

    def get_success_url(self):
        album_id = self.object.album_id
        return reverse_lazy('dashboards:galleryimage_list') + f'?album={album_id}'

# ---------------------- DownloadableFile ----------------------
class DownloadableFileListView(BaseAdminListView):
    model = DownloadableFile
    template_name = 'dashboards/crud/downloadablefile_list.html'
    context_object_name = 'items'

class DownloadableFileCreateView(BaseAdminCreateView):
    model = DownloadableFile
    fields = '__all__'
    template_name = 'dashboards/crud/downloadablefile_form.html'
    success_url = reverse_lazy('dashboards:downloadablefile_list')
    success_message = "Файл добавлен"

class DownloadableFileUpdateView(BaseAdminUpdateView):
    model = DownloadableFile
    fields = '__all__'
    template_name = 'dashboards/crud/downloadablefile_form.html'
    success_url = reverse_lazy('dashboards:downloadablefile_list')
    success_message = "Файл обновлен"

class DownloadableFileDeleteView(BaseAdminDeleteView):
    model = DownloadableFile
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:downloadablefile_list')
    success_message = "Файл удален"

# ---------------------- QuoteSection ----------------------
class QuoteSectionListView(BaseAdminListView):
    model = QuoteSection
    template_name = 'dashboards/crud/quotesection_list.html'
    context_object_name = 'items'

class QuoteSectionCreateView(BaseAdminCreateView):
    model = QuoteSection
    fields = '__all__'
    template_name = 'dashboards/crud/quotesection_form.html'
    success_url = reverse_lazy('dashboards:quotesection_list')
    success_message = "Цитата добавлена"

class QuoteSectionUpdateView(BaseAdminUpdateView):
    model = QuoteSection
    fields = '__all__'
    template_name = 'dashboards/crud/quotesection_form.html'
    success_url = reverse_lazy('dashboards:quotesection_list')
    success_message = "Цитата обновлена"

class QuoteSectionDeleteView(BaseAdminDeleteView):
    model = QuoteSection
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:quotesection_list')
    success_message = "Цитата удалена"

# ---------------------- Leadership ----------------------
class LeadershipListView(BaseAdminListView):
    model = Leadership
    template_name = 'dashboards/crud/leadership_list.html'
    context_object_name = 'items'

class LeadershipCreateView(BaseAdminCreateView):
    model = Leadership
    fields = '__all__'
    template_name = 'dashboards/crud/leadership_form.html'
    success_url = reverse_lazy('dashboards:leadership_list')
    success_message = "Руководитель добавлен"

class LeadershipUpdateView(BaseAdminUpdateView):
    model = Leadership
    fields = '__all__'
    template_name = 'dashboards/crud/leadership_form.html'
    success_url = reverse_lazy('dashboards:leadership_list')
    success_message = "Руководитель обновлен"

class LeadershipDeleteView(BaseAdminDeleteView):
    model = Leadership
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:leadership_list')
    success_message = "Руководитель удален"

# ---------------------- AcademyTeamMember ----------------------
class AcademyTeamMemberListView(BaseAdminListView):
    model = AcademyTeamMember
    template_name = 'dashboards/crud/team_list.html'
    context_object_name = 'items'

class AcademyTeamMemberCreateView(BaseAdminCreateView):
    model = AcademyTeamMember
    fields = '__all__'
    template_name = 'dashboards/crud/team_form.html'
    success_url = reverse_lazy('dashboards:team_list')
    success_message = "Член команды добавлен"

class AcademyTeamMemberUpdateView(BaseAdminUpdateView):
    model = AcademyTeamMember
    fields = '__all__'
    template_name = 'dashboards/crud/team_form.html'
    success_url = reverse_lazy('dashboards:team_list')
    success_message = "Член команды обновлен"

class AcademyTeamMemberDeleteView(BaseAdminDeleteView):
    model = AcademyTeamMember
    template_name = 'dashboards/crud/confirm_delete.html'
    success_url = reverse_lazy('dashboards:team_list')
    success_message = "Член команды удален"