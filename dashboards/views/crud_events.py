# dashboards/views/crud_events.py
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib import messages
from events.models import (
    Event, EventRegistration, InterestingProgram,
    NewsletterSubscription, PageSettings, Album, Photo
)
from .mixins import BaseAdminListView, BaseAdminCreateView, BaseAdminUpdateView, BaseAdminDeleteView
from PIL import Image
import os

# ----------------------------------------------------------------------
# Event
# ----------------------------------------------------------------------
class EventListView(BaseAdminListView):
    model = Event
    template_name = 'dashboards/crud/events/event_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.all().annotate(registrations_count=Count('registrations'))

class EventCreateView(BaseAdminCreateView):
    model = Event
    fields = '__all__'
    template_name = 'dashboards/crud/events/event_form.html'
    success_url = reverse_lazy('dashboards:event_list')
    success_message = "Мероприятие успешно создано"

class EventUpdateView(BaseAdminUpdateView):
    model = Event
    fields = '__all__'
    template_name = 'dashboards/crud/events/event_form.html'
    success_url = reverse_lazy('dashboards:event_list')
    success_message = "Мероприятие успешно обновлено"

class EventDeleteView(BaseAdminDeleteView):
    model = Event
    template_name = 'dashboards/crud/events/event_confirm_delete.html'
    success_url = reverse_lazy('dashboards:event_list')
    success_message = "Мероприятие удалено"

# ----------------------------------------------------------------------
# EventRegistration
# ----------------------------------------------------------------------
class EventRegistrationListView(BaseAdminListView):
    model = EventRegistration
    template_name = 'dashboards/crud/events/eventregistration_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        qs = EventRegistration.objects.all().select_related('event')
        event_id = self.request.GET.get('event')
        if event_id:
            qs = qs.filter(event_id=event_id)
        return qs

class EventRegistrationUpdateView(BaseAdminUpdateView):
    model = EventRegistration
    fields = ['full_name', 'phone', 'email', 'agreement']
    template_name = 'dashboards/crud/events/eventregistration_form.html'
    success_url = reverse_lazy('dashboards:eventregistration_list')
    success_message = "Регистрация обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registration_number'].disabled = True
        return form

class EventRegistrationDeleteView(BaseAdminDeleteView):
    model = EventRegistration
    template_name = 'dashboards/crud/events/eventregistration_confirm_delete.html'
    success_url = reverse_lazy('dashboards:eventregistration_list')
    success_message = "Регистрация удалена"

# ----------------------------------------------------------------------
# InterestingProgram
# ----------------------------------------------------------------------
class InterestingProgramListView(BaseAdminListView):
    model = InterestingProgram
    template_name = 'dashboards/crud/events/interestingprogram_list.html'
    context_object_name = 'items'

class InterestingProgramCreateView(BaseAdminCreateView):
    model = InterestingProgram
    fields = '__all__'
    template_name = 'dashboards/crud/events/interestingprogram_form.html'
    success_url = reverse_lazy('dashboards:interestingprogram_list')
    success_message = "Программа успешно добавлена"

class InterestingProgramUpdateView(BaseAdminUpdateView):
    model = InterestingProgram
    fields = '__all__'
    template_name = 'dashboards/crud/events/interestingprogram_form.html'
    success_url = reverse_lazy('dashboards:interestingprogram_list')
    success_message = "Программа успешно обновлена"

class InterestingProgramDeleteView(BaseAdminDeleteView):
    model = InterestingProgram
    template_name = 'dashboards/crud/events/interestingprogram_confirm_delete.html'
    success_url = reverse_lazy('dashboards:interestingprogram_list')
    success_message = "Программа удалена"

# ----------------------------------------------------------------------
# NewsletterSubscription
# ----------------------------------------------------------------------
class NewsletterSubscriptionListView(BaseAdminListView):
    model = NewsletterSubscription
    template_name = 'dashboards/crud/events/newslattersubscription_list.html'
    context_object_name = 'items'

class NewsletterSubscriptionUpdateView(BaseAdminUpdateView):
    model = NewsletterSubscription
    fields = ['is_active']
    template_name = 'dashboards/crud/events/newslattersubscription_form.html'
    success_url = reverse_lazy('dashboards:newslattersubscription_list')
    success_message = "Подписка обновлена"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].disabled = True
        return form

class NewsletterSubscriptionDeleteView(BaseAdminDeleteView):
    model = NewsletterSubscription
    template_name = 'dashboards/crud/events/newslattersubscription_confirm_delete.html'
    success_url = reverse_lazy('dashboards:newslattersubscription_list')
    success_message = "Подписка удалена"

# ----------------------------------------------------------------------
# PageSettings (singleton per page)
# ----------------------------------------------------------------------
class PageSettingsListView(BaseAdminListView):
    model = PageSettings
    template_name = 'dashboards/crud/events/pagesettings_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return PageSettings.objects.all()

class PageSettingsCreateView(BaseAdminCreateView):
    model = PageSettings
    fields = '__all__'
    template_name = 'dashboards/crud/events/pagesettings_form.html'
    success_url = reverse_lazy('dashboards:pagesettings_list')
    success_message = "Настройки страницы созданы"

    def dispatch(self, request, *args, **kwargs):
        page_name = request.POST.get('page_name') or request.GET.get('page_name')
        if page_name and PageSettings.objects.filter(page_name=page_name).exists():
            messages.error(request, f"Настройки для страницы '{page_name}' уже существуют. Вы можете только редактировать их.")
            return redirect('dashboards:pagesettings_list')
        return super().dispatch(request, *args, **kwargs)

class PageSettingsUpdateView(BaseAdminUpdateView):
    model = PageSettings
    fields = '__all__'
    template_name = 'dashboards/crud/events/pagesettings_form.html'
    success_url = reverse_lazy('dashboards:pagesettings_list')
    success_message = "Настройки страницы обновлены"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['page_name'].disabled = True
        return form

class PageSettingsDeleteView(BaseAdminDeleteView):
    model = PageSettings
    template_name = 'dashboards/crud/events/pagesettings_confirm_delete.html'
    success_url = reverse_lazy('dashboards:pagesettings_list')
    success_message = "Настройки страницы удалены"

# ----------------------------------------------------------------------
# Album
# ----------------------------------------------------------------------
class AlbumListView(BaseAdminListView):
    model = Album
    template_name = 'dashboards/crud/events/album_list.html'
    context_object_name = 'items'

class AlbumCreateView(BaseAdminCreateView):
    model = Album
    fields = '__all__'
    template_name = 'dashboards/crud/events/album_form.html'
    success_url = reverse_lazy('dashboards:album_list')
    success_message = "Альбом успешно создан"

class AlbumUpdateView(BaseAdminUpdateView):
    model = Album
    fields = '__all__'
    template_name = 'dashboards/crud/events/album_form.html'
    success_url = reverse_lazy('dashboards:album_list')
    success_message = "Альбом успешно обновлён"

class AlbumDeleteView(BaseAdminDeleteView):
    model = Album
    template_name = 'dashboards/crud/events/album_confirm_delete.html'
    success_url = reverse_lazy('dashboards:album_list')
    success_message = "Альбом удалён"

# ----------------------------------------------------------------------
# Photo – с поддержкой множественной загрузки
# ----------------------------------------------------------------------
class PhotoListView(BaseAdminListView):
    model = Photo
    template_name = 'dashboards/crud/events/photo_list.html'
    context_object_name = 'items'
    paginate_by = 30

    def get_queryset(self):
        qs = Photo.objects.all().select_related('album')
        album_id = self.request.GET.get('album')
        if album_id:
            qs = qs.filter(album_id=album_id)
        return qs

class PhotoCreateView(BaseAdminCreateView):
    model = Photo
    fields = ['album', 'title', 'description', 'order', 'is_active', 'image']
    template_name = 'dashboards/crud/events/photo_form.html'
    success_url = reverse_lazy('dashboards:photo_list')
    success_message = "Фотографии успешно добавлены"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multiple_files'] = True
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.image = None
        self.object.save()

        files = self.request.FILES.getlist('images')
        if not files:
            messages.error(self.request, "Вы не выбрали ни одного файла.")
            return self.form_invalid(form)

        created_count = 0
        for f in files:
            try:
                img = Image.open(f)
                img.verify()
                f.seek(0)

                Photo.objects.create(
                    album=self.object.album,
                    title=form.cleaned_data.get('title', ''),
                    description=form.cleaned_data.get('description', ''),
                    order=form.cleaned_data.get('order', 0),
                    is_active=form.cleaned_data.get('is_active', True),
                    image=f
                )
                created_count += 1
            except Exception as e:
                messages.warning(self.request, f"Ошибка при обработке файла {f.name}: {e}")

        self.object.delete()

        if created_count:
            messages.success(self.request, f"✅ Добавлено {created_count} фотографий.")
        else:
            messages.error(self.request, "Не удалось добавить ни одной фотографии.")
        return redirect(self.get_success_url())

class PhotoUpdateView(BaseAdminUpdateView):
    model = Photo
    fields = '__all__'
    template_name = 'dashboards/crud/events/photo_form.html'
    success_url = reverse_lazy('dashboards:photo_list')
    success_message = "Фотография успешно обновлена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multiple_files'] = False
        return context

class PhotoDeleteView(BaseAdminDeleteView):
    model = Photo
    template_name = 'dashboards/crud/events/photo_confirm_delete.html'
    success_url = reverse_lazy('dashboards:photo_list')
    success_message = "Фотография удалена"