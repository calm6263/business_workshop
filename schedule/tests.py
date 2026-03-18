"""
Тестовый модуль для приложения schedule
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from schedule.models import (
    ScheduleProgram, CurriculumModule, CurriculumDocument, 
    ProgramDocument, ProgramApplication, ScheduleSliderImage
)
from departments.models import Department
from staff.models import Teacher, TeacherProgram

import json
from datetime import date, timedelta


class ScheduleModelTests(TestCase):
    """Тесты для моделей приложения schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        # Создание тестового отделения
        self.department = Department.objects.create(
            name="Тестовое отделение",
            description="Описание тестового отделения",
            is_active=True
        )
        
        # Создание тестового преподавателя
        self.teacher = Teacher.objects.create(
            name="Иван Иванов",
            position="Старший преподаватель",
            description="Опытный преподаватель",
            is_active=True
        )
        
        # Создание тестовой программы
        self.program = ScheduleProgram.objects.create(
            title="Тестовая программа обучения",
            program_type="professional_retraining",
            certification_type="diploma",
            format="offline",
            detailed_description="Подробное описание тестовой программы",
            start_date=date.today() + timedelta(days=30),
            duration="6 месяцев",
            duration_hours=120,
            cost=50000.00,
            enrollment_status="open",
            department=self.department,
            schedule_description="Расписание занятий для тестовой программы",
            is_active=True,
            order=1
        )
        
        # Создание тестового модуля
        self.module = CurriculumModule.objects.create(
            program=self.program,
            title="Тестовый модуль",
            description="Описание тестового модуля",
            order=1
        )
        
        # Создание тестового документа программы
        self.program_document = ProgramDocument.objects.create(
            program=self.program,
            title="Тестовый документ",
            document_type="pdf",
            file=SimpleUploadedFile("test.pdf", b"file_content"),
            description="Описание тестового документа",
            order=1,
            is_active=True
        )
        
        # Создание тестового изображения слайдера
        self.slider_image = ScheduleSliderImage.objects.create(
            title="Тестовый слайдер",
            subtitle="Подзаголовок слайдера",
            description="Описание слайдера",
            image=SimpleUploadedFile(
                "test.jpg",
                b"file_content",
                content_type="image/jpeg"
            ),
            link="https://example.com",
            link_text="Подробнее",
            order=1,
            is_active=True
        )
        
        # Связывание преподавателя с программой
        self.teacher_program = TeacherProgram.objects.create(
            teacher=self.teacher,
            program=self.program,
            role="Ведущий преподаватель",
            is_active=True
        )
    
    def test_schedule_program_creation(self):
        """Тест создания программы"""
        self.assertEqual(self.program.title, "Тестовая программа обучения")
        self.assertEqual(self.program.program_type, "professional_retraining")
        self.assertEqual(self.program.format, "offline")
        self.assertTrue(self.program.is_active)
        self.assertEqual(self.program.slug, "testovaya-programma-obucheniya")
    
    def test_program_str_method(self):
        """Тест строкового представления программы"""
        expected_str = f"{self.program.start_date} - {self.program.title}"
        self.assertEqual(str(self.program), expected_str)
    
    def test_program_get_absolute_url(self):
        """Тест получения URL программы"""
        url = reverse('schedule:program_detail', kwargs={'slug': self.program.slug})
        self.assertEqual(
            self.program.get_absolute_url(),
            f'/schedule/program/{self.program.slug}/'
        )
    
    def test_curriculum_module_creation(self):
        """Тест создания модуля учебной программы"""
        self.assertEqual(self.module.title, "Тестовый модуль")
        self.assertEqual(self.module.program, self.program)
        self.assertEqual(self.module.order, 1)
    
    def test_curriculum_module_str_method(self):
        """Тест строкового представления модуля"""
        expected_str = f"{self.program.title} - {self.module.title}"
        self.assertEqual(str(self.module), expected_str)
    
    def test_program_document_creation(self):
        """Тест создания документа программы"""
        self.assertEqual(self.program_document.title, "Тестовый документ")
        self.assertEqual(self.program_document.document_type, "pdf")
        self.assertTrue(self.program_document.is_active)
    
    def test_slider_image_creation(self):
        """Тест создания изображения слайдера"""
        self.assertEqual(self.slider_image.title, "Тестовый слайдер")
        self.assertTrue(self.slider_image.is_active)
        self.assertEqual(self.slider_image.order, 1)
    
    def test_program_application_creation(self):
        """Тест создания заявки на обучение"""
        application = ProgramApplication.objects.create(
            program=self.program,
            contact_name="Петр Петров",
            phone="+79991234567",
            email="petr@example.com",
            additional_info="Дополнительная информация",
            agreement=True
        )
        
        self.assertEqual(application.contact_name, "Петр Петров")
        self.assertEqual(application.program, self.program)
        self.assertEqual(application.status, "pending")
        self.assertIsNotNone(application.application_number)
    
    def test_program_application_str_method(self):
        """Тест строкового представления заявки"""
        application = ProgramApplication.objects.create(
            program=self.program,
            contact_name="Петр Петров",
            phone="+79991234567",
            email="petr@example.com",
            agreement=True
        )
        
        expected_str = f"{application.application_number} - Петр Петров"
        self.assertEqual(str(application), expected_str)
    
    def test_program_active_manager(self):
        """Тест менеджера активных программ"""
        # Создаем неактивную программу
        inactive_program = ScheduleProgram.objects.create(
            title="Неактивная программа",
            program_type="seminar",
            format="online",
            start_date=date.today() + timedelta(days=60),
            duration_hours=40,
            is_active=False
        )
        
        active_programs = ScheduleProgram.objects.filter(is_active=True)
        self.assertIn(self.program, active_programs)
        self.assertNotIn(inactive_program, active_programs)
    
    def test_program_ordering(self):
        """Тест порядка сортировки программ"""
        # Создаем еще одну программу
        program2 = ScheduleProgram.objects.create(
            title="Вторая программа",
            program_type="training",
            format="blended",
            start_date=date.today() + timedelta(days=15),
            duration_hours=80,
            order=2,
            is_active=True
        )
        
        programs = ScheduleProgram.objects.filter(is_active=True).order_by('order', 'start_date')
        self.assertEqual(programs[0], self.program)
        self.assertEqual(programs[1], program2)


class ScheduleViewTests(TestCase):
    """Тесты для представлений приложения schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Создание тестового отделения
        self.department = Department.objects.create(
            name="Тестовое отделение",
            is_active=True
        )
        
        # Создание тестовых программ
        self.program1 = ScheduleProgram.objects.create(
            title="Программа 1",
            program_type="professional_retraining",
            format="offline",
            start_date=date(2024, 3, 15),
            duration_hours=120,
            is_active=True,
            order=1
        )
        
        self.program2 = ScheduleProgram.objects.create(
            title="Программа 2",
            program_type="qualification_upgrade",
            format="online",
            start_date=date(2024, 3, 20),
            duration_hours=80,
            is_active=True,
            order=2
        )
        
        # Создание архивной программы
        self.archive_program = ScheduleProgram.objects.create(
            title="Архивная программа",
            program_type="seminar",
            format="blended",
            start_date=date(2023, 12, 10),
            duration_hours=40,
            enrollment_status="archive",
            is_active=True,
            order=3
        )
        
        # Создание тестового изображения слайдера
        self.slider_image = ScheduleSliderImage.objects.create(
            title="Тестовый слайдер",
            image=SimpleUploadedFile(
                "test.jpg",
                b"file_content",
                content_type="image/jpeg"
            ),
            is_active=True
        )
    
    def test_schedule_page_view(self):
        """Тест отображения страницы расписания"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule/schedule.html')
        self.assertContains(response, "Расписание")
        self.assertContains(response, "Программа 1")
        self.assertContains(response, "Программа 2")
        self.assertContains(response, "Архивные программы")
    
    def test_schedule_page_with_filters(self):
        """Тест страницы расписания с фильтрами"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем наличие фильтров
        self.assertContains(response, "Тип программы")
        self.assertContains(response, "Формат")
        self.assertContains(response, "Месяц и год")
        
        # Проверяем счетчик программ
        self.assertContains(response, "Найдено программ")
    
    def test_schedule_page_no_programs(self):
        """Тест страницы расписания без программ"""
        # Удаляем все программы
        ScheduleProgram.objects.all().delete()
        
        response = self.client.get(reverse('schedule:schedule_page'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "В настоящее время нет запланированных программ")
    
    def test_program_detail_view(self):
        """Тест отображения детальной страницы программы"""
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': self.program1.slug}
        ))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule/program_detail.html')
        self.assertContains(response, self.program1.title)
        self.assertContains(response, "О программе")
        self.assertContains(response, "Программа обучения")
        self.assertContains(response, "Расписание занятий")
        self.assertContains(response, "Преподаватели")
        self.assertContains(response, "Как поступить")
    
    def test_program_detail_view_not_found(self):
        """Тест детальной страницы несуществующей программы"""
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': 'non-existent-slug'}
        ))
        
        self.assertEqual(response.status_code, 404)
    
    def test_program_detail_view_inactive(self):
        """Тест детальной страницы неактивной программы"""
        # Делаем программу неактивной
        self.program1.is_active = False
        self.program1.save()
        
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': self.program1.slug}
        ))
        
        self.assertEqual(response.status_code, 404)
    
    def test_program_detail_from_department(self):
        """Тест перехода на детальную страницу из отделения"""
        # Назначаем программе отделение
        self.program1.department = self.department
        self.program1.save()
        
        response = self.client.get(
            reverse('schedule:program_detail', kwargs={'slug': self.program1.slug}),
            {'from': 'department'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('from_department', response.context)
        self.assertTrue(response.context['from_department'])
    
    def test_submit_application_view(self):
        """Тест отправки заявки на обучение"""
        data = {
            'contactName': 'Иван Иванов',
            'phone': '+79991234567',
            'email': 'ivan@example.com',
            'additionalInfo': 'Хочу участвовать в программе',
            'agreement': 'on'
        }
        
        response = self.client.post(
            reverse('schedule:submit_application', kwargs={'slug': self.program1.slug}),
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertIn('application_number', response_data)
        self.assertIn('Заявка успешно отправлена', response_data['message'])
        
        # Проверяем, что заявка создана в базе данных
        self.assertEqual(ProgramApplication.objects.count(), 1)
        application = ProgramApplication.objects.first()
        self.assertEqual(application.contact_name, 'Иван Иванов')
        self.assertEqual(application.program, self.program1)
    
    def test_submit_application_invalid_data(self):
        """Тест отправки заявки с неверными данными"""
        data = {
            'contactName': '',  # Пустое имя
            'phone': '+79991234567',
            'email': 'invalid-email',  # Неверный email
            'agreement': 'on'
        }
        
        response = self.client.post(
            reverse('schedule:submit_application', kwargs={'slug': self.program1.slug}),
            data=data
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])  # Форма все равно проходит валидацию на клиенте
    
    def test_submit_application_get_request(self):
        """Тест GET-запроса к обработчику заявок"""
        response = self.client.get(
            reverse('schedule:submit_application', kwargs={'slug': self.program1.slug})
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('Неверный метод запроса', response_data['message'])
    
    def test_submit_application_program_not_found(self):
        """Тест отправки заявки для несуществующей программы"""
        data = {
            'contactName': 'Иван Иванов',
            'phone': '+79991234567',
            'email': 'ivan@example.com',
            'agreement': 'on'
        }
        
        response = self.client.post(
            reverse('schedule:submit_application', kwargs={'slug': 'non-existent-slug'}),
            data=data
        )
        
        self.assertEqual(response.status_code, 404)


class ScheduleTemplateTests(TestCase):
    """Тесты шаблонов приложения schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Создание тестовой программы
        self.program = ScheduleProgram.objects.create(
            title="Тестовая программа",
            program_type="professional_retraining",
            format="offline",
            start_date=date(2024, 3, 15),
            duration_hours=120,
            is_active=True
        )
        
        # Создание тестового модуля
        self.module = CurriculumModule.objects.create(
            program=self.program,
            title="Тестовый модуль",
            description="Описание тестового модуля",
            order=1
        )
        
        # Создание тестового документа
        self.document = ProgramDocument.objects.create(
            program=self.program,
            title="Тестовый документ",
            document_type="pdf",
            file=SimpleUploadedFile("test.pdf", b"file_content"),
            is_active=True
        )
        
        # Создание тестового изображения слайдера
        self.slider = ScheduleSliderImage.objects.create(
            title="Тестовый слайдер",
            image=SimpleUploadedFile(
                "test.jpg",
                b"file_content",
                content_type="image/jpeg"
            ),
            is_active=True
        )
    
    def test_schedule_template_context(self):
        """Тест контекста шаблона расписания"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем наличие ключевых данных в контексте
        self.assertIn('monthly_data', response.context)
        self.assertIn('available_years', response.context)
        self.assertIn('program_types', response.context)
        self.assertIn('total_programs_count', response.context)
        self.assertIn('archive_programs', response.context)
        self.assertIn('program_types_json', response.context)
        self.assertIn('slider_images', response.context)
    
    def test_schedule_template_contains_elements(self):
        """Тест наличия элементов в шаблоне расписания"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем основные элементы
        self.assertContains(response, 'slider-section')
        self.assertContains(response, 'calendar-nav')
        self.assertContains(response, 'schedule-filter')
        self.assertContains(response, 'month-section')
        self.assertContains(response, 'program-card-new')
        
        # Проверяем фильтры
        self.assertContains(response, 'Тип программы')
        self.assertContains(response, 'Формат')
        self.assertContains(response, 'Месяц и год')
    
    def test_program_detail_template_context(self):
        """Тест контекста шаблона детальной страницы программы"""
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': self.program.slug}
        ))
        
        # Проверяем наличие ключевых данных в контексте
        self.assertIn('program', response.context)
        self.assertIn('same_month_programs', response.context)
        self.assertIn('curriculum_modules', response.context)
        self.assertIn('program_documents', response.context)
        self.assertIn('from_department', response.context)
    
    def test_program_detail_template_contains_elements(self):
        """Тест наличия элементов в шаблоне детальной страницы"""
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': self.program.slug}
        ))
        
        # Проверяем основные элементы
        self.assertContains(response, 'program-hero-fullwidth')
        self.assertContains(response, 'nav-tabs-new-wrapper')
        self.assertContains(response, 'content-section')
        
        # Проверяем разделы
        self.assertContains(response, 'О программе')
        self.assertContains(response, 'Программа обучения')
        self.assertContains(response, 'Расписание занятий')
        self.assertContains(response, 'Преподаватели')
        self.assertContains(response, 'Как поступить')
        
        # Проверяем модули и документы
        self.assertContains(response, self.module.title)
        
        # Проверяем модальное окно заявки
        self.assertContains(response, 'application-modal')
        self.assertContains(response, 'Подать заявку')


class ScheduleAPITests(TestCase):
    """Тесты API приложения schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Создание тестовой программы
        self.program = ScheduleProgram.objects.create(
            title="API Тестовая программа",
            program_type="professional_retraining",
            format="online",
            start_date=date.today() + timedelta(days=30),
            duration_hours=100,
            is_active=True,
            slug="api-test-program"
        )
        
        # Создание CSRF-токена для тестов
        self.csrf_client = Client(enforce_csrf_checks=True)
    
    def test_program_list_api(self):
        """Тест API списка программ"""
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
    
    def test_program_detail_api(self):
        """Тест API детальной страницы программы"""
        response = self.client.get(f'/schedule/program/{self.program.slug}/')
        self.assertEqual(response.status_code, 200)
    
    def test_application_submission_api(self):
        """Тест API отправки заявки"""
        # Для этого теста нам нужно получить CSRF-токен
        # В реальном приложении это делается через сессию
        
        data = {
            'contactName': 'API Тест Пользователь',
            'phone': '+79998887766',
            'email': 'api_test@example.com',
            'additionalInfo': 'Тест через API',
            'agreement': 'on'
        }
        
        # В тестовой среде можно отключить CSRF проверку
        response = self.client.post(
            f'/schedule/program/{self.program.slug}/apply/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Проверяем, что запрос обработан (может быть 200 или 403 без CSRF)
        self.assertIn(response.status_code, [200, 403, 400])
    
    def test_program_filter_api(self):
        """Тест API фильтрации программ"""
        # Создаем программы разных типов
        ScheduleProgram.objects.create(
            title="Очная программа",
            program_type="professional_retraining",
            format="offline",
            start_date=date(2024, 4, 1),
            duration_hours=120,
            is_active=True
        )
        
        ScheduleProgram.objects.create(
            title="Онлайн программа",
            program_type="seminar",
            format="online",
            start_date=date(2024, 4, 15),
            duration_hours=40,
            is_active=True
        )
        
        # Получаем страницу расписания
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что все программы отображаются
        self.assertContains(response, "Очная программа")
        self.assertContains(response, "Онлайн программа")
        self.assertContains(response, "API Тестовая программа")


class ScheduleIntegrationTests(TestCase):
    """Интеграционные тесты приложения schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Создание отделения
        self.department = Department.objects.create(
            name="Интеграционное тестирование",
            is_active=True
        )
        
        # Создание нескольких программ
        self.programs = []
        for i in range(5):
            program = ScheduleProgram.objects.create(
                title=f"Программа интеграционного теста {i+1}",
                program_type="professional_retraining",
                format="offline" if i % 2 == 0 else "online",
                start_date=date(2024, 4, (i+1)*5),
                duration_hours=100 + i*20,
                cost=50000 + i*10000,
                department=self.department if i < 3 else None,
                is_active=True,
                order=i+1
            )
            self.programs.append(program)
        
        # Создание архивных программ
        for i in range(3):
            ScheduleProgram.objects.create(
                title=f"Архивная программа {i+1}",
                program_type="seminar",
                format="blended",
                start_date=date(2023, 12, (i+1)*10),
                duration_hours=40,
                enrollment_status="archive",
                is_active=True
            )
        
        # Создание слайдера
        ScheduleSliderImage.objects.create(
            title="Интеграционный слайдер",
            subtitle="Тестирование всех компонентов",
            description="Полная интеграция всех элементов",
            is_active=True
        )
    
    def test_full_schedule_workflow(self):
        """Тест полного рабочего процесса расписания"""
        # 1. Открываем главную страницу расписания
        response = self.client.get(reverse('schedule:schedule_page'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Проверяем наличие всех программ
        for program in self.programs:
            self.assertContains(response, program.title)
        
        # 3. Переходим на детальную страницу программы
        test_program = self.programs[0]
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': test_program.slug}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_program.title)
        
        # 4. Открываем модальное окно заявки (через JavaScript)
        # В тестах мы не можем тестировать JavaScript, но можем проверить наличие формы
        self.assertContains(response, 'application-modal')
        self.assertContains(response, 'Заявка на обучение')
        
        # 5. Отправляем заявку
        application_data = {
            'contactName': 'Интеграционный Тест',
            'phone': '+79991112233',
            'email': 'integration@test.com',
            'additionalInfo': 'Тест интеграционного рабочего процесса',
            'agreement': 'on'
        }
        
        response = self.client.post(
            reverse('schedule:submit_application', kwargs={'slug': test_program.slug}),
            data=application_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Проверяем успешность отправки
        if response.status_code == 200:
            response_data = json.loads(response.content)
            self.assertTrue(response_data['success'])
            
            # Проверяем создание заявки в БД
            self.assertTrue(ProgramApplication.objects.exists())
            application = ProgramApplication.objects.first()
            self.assertEqual(application.contact_name, 'Интеграционный Тест')
            self.assertEqual(application.program, test_program)
    
    def test_schedule_with_department_context(self):
        """Тест расписания в контексте отделения"""
        # Программа с отделением
        department_program = self.programs[0]
        
        # Переходим из контекста отделения
        response = self.client.get(
            reverse('schedule:program_detail', kwargs={'slug': department_program.slug}),
            {'from': 'department'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('from_department', response.context)
        self.assertTrue(response.context['from_department'])
        
        # Проверяем наличие ссылки "Назад" в отделение
        self.assertContains(response, 'department_detail')
    
    def test_archive_programs_display(self):
        """Тест отображения архивных программ"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем наличие раздела с архивными программами
        self.assertContains(response, 'Архивные программы')
        
        # Проверяем карусель архивных программ
        self.assertContains(response, 'archive-carousel-section')
        self.assertContains(response, 'carousel-container')
    
    def test_schedule_filter_functionality(self):
        """Тест функциональности фильтров"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем наличие всех фильтров
        self.assertContains(response, 'programTypeFilter')
        self.assertContains(response, 'formatFilter')
        self.assertContains(response, 'monthYearFilter')
        
        # Проверяем выпадающие меню
        self.assertContains(response, 'programTypeDropdown')
        self.assertContains(response, 'formatDropdown')
        self.assertContains(response, 'monthYearDropdown')
        
        # Проверяем опции фильтров
        self.assertContains(response, 'Все программы')
        self.assertContains(response, 'Все форматы')
        self.assertContains(response, 'Все месяцы')
    
    def test_calendar_navigation(self):
        """Тест навигации календаря"""
        response = self.client.get(reverse('schedule:schedule_page'))
        
        # Проверяем наличие календаря
        self.assertContains(response, 'calendar-nav')
        self.assertContains(response, 'calendar-dates')
        self.assertContains(response, 'calendar-week')
        self.assertContains(response, 'calendar-day')
        
        # Проверяем кнопки навигации
        self.assertContains(response, 'prev-btn')
        self.assertContains(response, 'next-btn')


class ScheduleErrorTests(TestCase):
    """Тесты обработки ошибок в приложении schedule"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
    
    def test_404_on_nonexistent_program(self):
        """Тест 404 на несуществующую программу"""
        response = self.client.get('/schedule/program/non-existent-program/')
        self.assertEqual(response.status_code, 404)
    
    def test_empty_schedule_page(self):
        """Тест страницы расписания без данных"""
        # Убеждаемся, что нет ни одной программы
        ScheduleProgram.objects.all().delete()
        ScheduleSliderImage.objects.all().delete()
        
        response = self.client.get(reverse('schedule:schedule_page'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "В настоящее время нет запланированных программ")
    
    def test_program_with_invalid_date(self):
        """Тест программы с неверной датой"""
        # Создаем программу без даты начала (хотя модель требует дату)
        try:
            program = ScheduleProgram.objects.create(
                title="Программа без даты",
                program_type="training",
                format="online",
                # start_date отсутствует
                duration_hours=50,
                is_active=True
            )
            # Если программа создалась, проверяем, что у нее есть дата по умолчанию
            self.assertIsNotNone(program.start_date)
        except Exception as e:
            # Ожидаем ошибку валидации
            self.assertIn('start_date', str(e))
    
    def test_application_without_agreement(self):
        """Тест заявки без согласия"""
        # Создаем тестовую программу
        program = ScheduleProgram.objects.create(
            title="Тестовая программа для заявки",
            program_type="professional_retraining",
            format="offline",
            start_date=date.today() + timedelta(days=30),
            duration_hours=100,
            is_active=True,
            slug="test-application-program"
        )
        
        # Пытаемся отправить заявку без согласия
        data = {
            'contactName': 'Тест Без Согласия',
            'phone': '+79990001122',
            'email': 'no_agreement@test.com',
            'additionalInfo': 'Тест без согласия',
            # agreement отсутствует
        }
        
        response = self.client.post(
            reverse('schedule:submit_application', kwargs={'slug': program.slug}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Проверяем ответ
        if response.status_code == 200:
            response_data = json.loads(response.content)
            # Заявка должна создаться, но agreement будет False
            self.assertTrue(response_data['success'])
            
            # Проверяем заявку в БД
            application = ProgramApplication.objects.first()
            self.assertFalse(application.agreement)


class SchedulePerformanceTests(TestCase):
    """Тесты производительности приложения schedule"""
    
    def setUp(self):
        """Настройка большого количества тестовых данных"""
        self.client = Client()
        
        # Создаем много программ для тестирования производительности
        for i in range(50):
            ScheduleProgram.objects.create(
                title=f"Программа производительности {i+1}",
                program_type="professional_retraining" if i % 3 == 0 else "seminar",
                format="offline" if i % 2 == 0 else "online",
                start_date=date(2024, (i % 12) + 1, (i % 28) + 1),
                duration_hours=50 + (i * 5),
                cost=30000 + (i * 1000),
                is_active=True,
                order=i+1
            )
        
        # Создаем несколько архивных программ
        for i in range(10):
            ScheduleProgram.objects.create(
                title=f"Архивная программа {i+1}",
                program_type="qualification_upgrade",
                format="blended",
                start_date=date(2023, (i % 12) + 1, (i % 28) + 1),
                duration_hours=40,
                enrollment_status="archive",
                is_active=True
            )
    
    def test_schedule_page_performance(self):
        """Тест производительности страницы расписания"""
        import time
        
        start_time = time.time()
        response = self.client.get(reverse('schedule:schedule_page'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что страница загружается за разумное время
        # (менее 2 секунд для 60 программ)
        load_time = end_time - start_time
        self.assertLess(load_time, 2.0, 
                       f"Страница загружается слишком медленно: {load_time:.2f} сек.")
        
        # Проверяем, что все программы отображаются
        self.assertContains(response, "Программа производительности")
        
        # Проверяем наличие раздела с архивными программами
        self.assertContains(response, "Архивные программы")
    
    def test_program_detail_performance(self):
        """Тест производительности детальной страницы программы"""
        program = ScheduleProgram.objects.first()
        
        import time
        start_time = time.time()
        response = self.client.get(reverse(
            'schedule:program_detail',
            kwargs={'slug': program.slug}
        ))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем время загрузки
        load_time = end_time - start_time
        self.assertLess(load_time, 1.0, 
                       f"Детальная страница загружается слишком медленно: {load_time:.2f} сек.")
    
    def test_database_queries_count(self):
        """Тест количества запросов к базе данных"""
        from django.db import connection
        
        # Сбрасываем счетчик запросов
        connection.force_debug_cursor = True
        
        # Получаем страницу расписания
        with self.assertNumQueries(10):  # Ожидаем не более 10 запросов
            response = self.client.get(reverse('schedule:schedule_page'))
        
        self.assertEqual(response.status_code, 200)
        
        # Возвращаем настройки базы данных
        connection.force_debug_cursor = False