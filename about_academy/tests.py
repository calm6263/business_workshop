from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import (
    ValuesSection, StatisticsSection, PhotoAlbum, GalleryImage,
    LeaderSpeech, LeaderSpeechVideo, MainSlider, DownloadableFile, ContactMessage
)


class AboutAcademyModelsTest(TestCase):
    def setUp(self):
        self.values = ValuesSection.objects.create(
            title="Наши ценности",
            quote_1="Цитата 1",
            quote_2="Цитата 2",
            content="Дополнительный контент",
            order=1,
            is_active=True
        )

        self.stats = StatisticsSection.objects.create(
            title="Академия в цифрах",
            stat_title="Статистика",
            stat_number_1="1000",
            stat_label_1="Учеников",
            order=1,
            is_active=True
        )

        self.leader_speech = LeaderSpeech.objects.create(
            title="Речь руководителя",
            is_active=True,
            order=1
        )

        self.slider = MainSlider.objects.create(
            title="Главный слайд",
            description="Описание слайда",
            order=1,
            is_active=True,
            image=SimpleUploadedFile("slider.jpg", b"file_content", content_type="image/jpeg")
        )

        self.album = PhotoAlbum.objects.create(
            title="Тестовый альбом",
            description="Описание альбома",
            order=1,
            is_active=True,
            cover_image=SimpleUploadedFile("cover.jpg", b"file_content", content_type="image/jpeg")
        )

        self.gallery_image = GalleryImage.objects.create(
            album=self.album,
            caption="Подпись к фото",
            description="Описание фото",
            order=1,
            is_active=True,
            image=SimpleUploadedFile("gallery.jpg", b"file_content", content_type="image/jpeg")
        )

        self.download_file = DownloadableFile.objects.create(
            title="Презентация",
            description="Файл для скачивания",
            file_type='pdf',
            button_text="Скачать",
            order=1,
            is_active=True,
            position_right=True,
            file=SimpleUploadedFile("test.pdf", b"PDF content", content_type="application/pdf")
        )

    def test_values_section_str(self):
        self.assertEqual(str(self.values), "Наши ценности")

    def test_statistics_section_str(self):
        self.assertEqual(str(self.stats), "Академия в цифрах")

    def test_photo_album_str(self):
        self.assertEqual(str(self.album), "Тестовый альбом")

    def test_gallery_image_str(self):
        self.assertIn("Подпись к фото", str(self.gallery_image))

    def test_leader_speech_str(self):
        self.assertEqual(str(self.leader_speech), "Речь руководителя")

    def test_main_slider_str(self):
        self.assertIn("Главный слайд", str(self.slider))

    def test_downloadable_file_str(self):
        self.assertEqual(str(self.download_file), "Презентация")

    def test_downloadable_file_get_file_icon(self):
        self.assertEqual(self.download_file.get_file_icon(), 'fa-file-pdf')

    def test_leader_speech_video_get_video_source(self):
        video = LeaderSpeechVideo.objects.create(
            leader_speech=self.leader_speech,
            title="Видео",
            video_url="https://youtube.com/watch?v=test",
            order=1,
            is_active=True
        )
        self.assertEqual(video.get_video_source(), "https://youtube.com/watch?v=test")


class AboutAcademyViewsTest(TestCase):
    def setUp(self):
        self.album = PhotoAlbum.objects.create(
            title="Альбом для просмотра",
            description="Описание",
            order=1,
            is_active=True,
            cover_image=SimpleUploadedFile("cover.jpg", b"file_content", content_type="image/jpeg")
        )
        GalleryImage.objects.create(
            album=self.album,
            caption="Фото 1",
            order=1,
            is_active=True,
            image=SimpleUploadedFile("img1.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_about_academy_view_status_code(self):
        response = self.client.get(reverse('about_academy'))
        self.assertEqual(response.status_code, 200)

    def test_about_academy_template_used(self):
        response = self.client.get(reverse('about_academy'))
        self.assertTemplateUsed(response, 'about_academy/about_academy.html')

    def test_about_academy_context_data(self):
        response = self.client.get(reverse('about_academy'))
        self.assertIn('main_slider', response.context)
        self.assertIn('photo_albums', response.context)
        self.assertIn('downloadable_files', response.context)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Об академии')

    def test_album_detail_view_status_code(self):
        response = self.client.get(reverse('album_detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)

    def test_album_detail_template_used(self):
        response = self.client.get(reverse('album_detail', args=[self.album.id]))
        self.assertTemplateUsed(response, 'about_academy/album_detail.html')

    def test_album_detail_context(self):
        response = self.client.get(reverse('album_detail', args=[self.album.id]))
        self.assertEqual(response.context['album'], self.album)
        self.assertEqual(response.context['images'].count(), 1)
        self.assertIn('title', response.context)
        self.assertIn(self.album.title, response.context['title'])

    def test_album_detail_inactive_album_404(self):
        inactive_album = PhotoAlbum.objects.create(
            title="Неактивный",
            is_active=False,
            cover_image=SimpleUploadedFile("cover.jpg", b"file_content", content_type="image/jpeg")
        )
        response = self.client.get(reverse('album_detail', args=[inactive_album.id]))
        self.assertEqual(response.status_code, 404)


class ContactFormTest(TestCase):
    def test_contact_form_valid_submission(self):
        response = self.client.post(reverse('about_academy'), {
            'name': 'Иван Иванов',
            'email': 'ivan@example.com',
            'message': 'Тестовое сообщение',
            'not_robot': 'on'
        })
        self.assertEqual(response.status_code, 302)  # Redirect بعد النجاح
        self.assertEqual(ContactMessage.objects.count(), 1)

        message = ContactMessage.objects.first()
        self.assertEqual(message.name, 'Иван Иванов')
        self.assertEqual(message.email, 'ivan@example.com')
        self.assertEqual(message.message, 'Тестовое сообщение')
        self.assertTrue(message.is_robot)

        # تحقق من رسالة النجاح بعد التوجيه
        follow_response = self.client.get(reverse('about_academy'))
        self.assertContains(follow_response, 'Спасибо! Ваше сообщение успешно отправлено.')

    def test_contact_form_invalid_submission(self):
        # إرسال نموذج غير صالح
        response = self.client.post(reverse('about_academy'), {
            'name': '',
            'email': 'invalid',
            'message': '',
            'not_robot': ''
        })

        # يجب أن يبقى في نفس الصفحة مع status 200
        self.assertEqual(response.status_code, 200)

        # لا يتم إنشاء رسالة في قاعدة البيانات
        self.assertEqual(ContactMessage.objects.count(), 0)

        # التحقق من ظهور رسالة الخطأ مباشرة في الـ response بعد الـ POST
        self.assertContains(response, 'Пожалуйста, заполните все поля и подтвердите, что вы не робот.')


class AboutAcademyAdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        self.client.login(username='admin', password='testpass123')

    def test_admin_access(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_models_registered(self):
        response = self.client.get('/admin/about_academy/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Разделы &#x27;Наши ценности&#x27;')
        self.assertContains(response, 'Фотоальбомы')
        self.assertContains(response, 'Файлы для скачивания')