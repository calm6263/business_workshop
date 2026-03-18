# dashboards/views/dashboard.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Импорты всех моделей для статистики
from main.models import Slide, License
from about_academy.models import (
    MainSlider, ValuesSection, StatisticsSection, LeaderSpeech,
    PhotoAlbum, DownloadableFile, QuoteSection, Leadership, AcademyTeamMember
)
from applicants.models import (
    ApplicantsPage, ApplicationMethod, EnrollmentStage,
    ApplicantDocument, ApplicantApplication
)
from consultations.models import ConsultationRequest, HeroSlide, FAQ, SuccessPageImage
from contacts.models import (
    ContactSection, OrganizationInfo, SocialMedia,
    ContactPageSettings, ContactHero
)
from departments.models import Department, HeroImage
from press_center.models import PressCenterPage, PressCenterImage, PublicationRequest
from events.models import (
    Event, EventRegistration, InterestingProgram,
    NewsletterSubscription, PageSettings, Album, Photo
)
from partners.models import HomePageSlider, Partner, PartnershipApplication, LogoCarousel
from fta_journal.models import JournalIssue, SliderImage, SectionSettings, IssuePage
from news.models import News, Category, NewsPageHero, Subscriber
from projects.models import (
    Project, ProjectCategory, ProjectMember, ProjectPartner,
    ProjectSlide, ContactRequest, ProjectProposal, ProjectGallery,
    ProjectJoinRequest
)
from schedule.models import (
    ScheduleProgram, CurriculumModule, CurriculumDocument,
    ProgramApplication, ScheduleSliderImage, CalendarSliderImage
)
from research.models import (
    ResearchCategory, Research, ResearchTag, ResearchHero,
    Conference, ConferenceRegistration,
    YouthCouncilDepartment, YouthCouncilMember
)
from single_window.models import BasicInfo, Slider, FAQ as SingleWindowFAQ, ServiceRequest
from staff.models import TeamMember, TeacherProgram, PageHero
from contact_form.models import ContactMessage
from patents.models import PatentImage


@method_decorator(never_cache, name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')

    def get_template_names(self):
        user = self.request.user
        if hasattr(user, 'profile'):
            user_type = user.profile.user_type
            templates_map = {
                'admin': 'dashboards/admin_dashboard.html',
                'teacher': 'dashboards/teacher_dashboard.html',
                'student': 'dashboards/student_dashboard.html',
                'company': 'dashboards/company_dashboard.html',
                'regular': 'dashboards/regular_dashboard.html',
            }
            return [templates_map.get(user_type, 'dashboards/regular_dashboard.html')]
        return ['dashboards/regular_dashboard.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        company = None
        if hasattr(user, 'profile') and user.profile.user_type == 'company' and user.profile.company:
            company = user.profile.company

        # ========== Helper function لتصفية الكونت حسب الشركة ==========
        def filter_by_company(queryset):
            if company:
                if hasattr(queryset.model, 'company'):
                    return queryset.filter(company=company)
            return queryset

        # ========== Общее количество заявок и заявок в обработке ==========
        total_apps = 0
        pending_apps = 0

        # ApplicantApplication
        qs_applicant = filter_by_company(ApplicantApplication.objects.all())
        total_apps += qs_applicant.count()
        pending_apps += qs_applicant.filter(status='pending').count()

        # ConsultationRequest
        qs_consult = filter_by_company(ConsultationRequest.objects.all())
        total_apps += qs_consult.count()
        pending_apps += qs_consult.filter(is_processed=False).count()

        # PartnershipApplication
        qs_partner = filter_by_company(PartnershipApplication.objects.all())
        total_apps += qs_partner.count()
        pending_apps += qs_partner.filter(status='pending').count()

        # ServiceRequest
        qs_service = filter_by_company(ServiceRequest.objects.all())
        total_apps += qs_service.count()
        pending_apps += qs_service.filter(status='new').count()

        # ProjectProposal
        qs_proposal = filter_by_company(ProjectProposal.objects.all())
        total_apps += qs_proposal.count()
        pending_apps += qs_proposal.filter(status='pending').count()

        # ProjectJoinRequest
        qs_join = filter_by_company(ProjectJoinRequest.objects.all())
        total_apps += qs_join.count()
        pending_apps += qs_join.filter(status='pending').count()

        # ProgramApplication
        qs_program = filter_by_company(ProgramApplication.objects.all())
        total_apps += qs_program.count()
        pending_apps += qs_program.filter(status='pending').count()

        # ConferenceRegistration
        qs_conf_reg = filter_by_company(ConferenceRegistration.objects.all())
        total_apps += qs_conf_reg.count()
        if hasattr(ConferenceRegistration, 'status'):
            pending_apps += qs_conf_reg.filter(status='pending').count()

        # PublicationRequest
        qs_pub = filter_by_company(PublicationRequest.objects.all())
        total_apps += qs_pub.count()
        pending_apps += qs_pub.filter(status='pending').count()

        # ContactMessage
        qs_contact = filter_by_company(ContactMessage.objects.all())
        total_apps += qs_contact.count()
        pending_apps += qs_contact.filter(is_read=False).count()

        context['total_applications'] = total_apps
        context['pending_applications'] = pending_apps

        # Последние 5 заявок (пример из ApplicantApplication)
        context['recent_applications'] = qs_applicant.order_by('-created_at')[:5]

        # Количество непрочитанных сообщений обратной связи
        context['unread_contact_messages'] = qs_contact.filter(is_read=False).count()

        # ========== Данные для администратора ==========
        if hasattr(user, 'profile'):
            user_type = user.profile.user_type
            if user_type == 'company' and company:
                context['company'] = company

            if user_type == 'admin':
                # MAIN (INDEX) – هذه البيانات عامة ولا ترتبط بشركة
                context['slides_count'] = Slide.objects.filter(is_active=True).count()
                context['licenses_count'] = License.objects.filter(is_active=True).count()

                # about_academy – عام
                context['main_slider_items'] = MainSlider.objects.filter(is_active=True).order_by('order')
                context['values_sections'] = ValuesSection.objects.filter(is_active=True).order_by('order')
                context['statistics_sections'] = StatisticsSection.objects.filter(is_active=True).order_by('order')
                context['leader_speeches'] = LeaderSpeech.objects.filter(is_active=True).order_by('order')
                context['photo_albums'] = PhotoAlbum.objects.filter(is_active=True).order_by('order')
                context['downloadable_files'] = DownloadableFile.objects.filter(is_active=True).order_by('order')
                context['quote_sections'] = QuoteSection.objects.filter(is_active=True).order_by('order')
                context['leadership_members'] = Leadership.objects.filter(is_active=True).order_by('order')
                context['team_members'] = AcademyTeamMember.objects.filter(is_active=True).order_by('department', 'rank', 'order')[:10]

                # applicants – بعضها عام وبعضها خاص (لكن في admin نعرض الكل)
                context['applicants_page'] = ApplicantsPage.objects.first()
                context['application_methods_count'] = ApplicationMethod.objects.count()
                context['enrollment_stages_count'] = EnrollmentStage.objects.count()
                context['applicant_documents_count'] = ApplicantDocument.objects.count()
                context['applicant_applications_count'] = ApplicantApplication.objects.count()

                # consultations – عام
                context['consultation_requests_count'] = ConsultationRequest.objects.count()
                context['hero_slides_count'] = HeroSlide.objects.count()
                context['faqs_count'] = FAQ.objects.count()
                context['success_images_count'] = SuccessPageImage.objects.count()

                # contacts – عام
                context['contact_sections_count'] = ContactSection.objects.count()
                context['organization_info_exists'] = OrganizationInfo.objects.exists()
                if OrganizationInfo.objects.exists():
                    context['organization_info_pk'] = OrganizationInfo.objects.first().pk
                context['social_media_count'] = SocialMedia.objects.count()
                context['page_settings_exists'] = ContactPageSettings.objects.exists()
                if ContactPageSettings.objects.exists():
                    context['page_settings_pk'] = ContactPageSettings.objects.first().pk
                context['contact_hero_count'] = ContactHero.objects.count()

                # departments – عام
                context['departments_count'] = Department.objects.count()
                context['hero_images_count'] = HeroImage.objects.count()

                # events – يمكن تصفيتها حسب الشركة إذا أردنا، لكن في admin نعرض الكل
                context['events_count'] = Event.objects.count()
                context['event_registrations_count'] = EventRegistration.objects.count()
                context['interesting_programs_count'] = InterestingProgram.objects.count()
                context['newsletter_subscriptions_count'] = NewsletterSubscription.objects.count()
                context['page_settings_count'] = PageSettings.objects.count()
                context['albums_count'] = Album.objects.count()
                context['photos_count'] = Photo.objects.count()

                # fta_journal – عام
                context['journal_issues_count'] = JournalIssue.objects.count()
                context['journal_slider_images_count'] = SliderImage.objects.count()
                context['journal_section_settings_exists'] = SectionSettings.objects.exists()
                if SectionSettings.objects.exists():
                    context['journal_section_settings_pk'] = SectionSettings.objects.first().pk
                context['journal_pages_count'] = IssuePage.objects.count()

                # news – عام
                context['news_count'] = News.objects.count()
                context['categories_count'] = Category.objects.count()
                context['hero_count'] = NewsPageHero.objects.count()
                context['subscribers_count'] = Subscriber.objects.count()

                # partners – عام
                context['home_sliders_count'] = HomePageSlider.objects.count()
                context['partners_count'] = Partner.objects.count()
                context['applications_count'] = PartnershipApplication.objects.count()
                context['logo_carousel_count'] = LogoCarousel.objects.count()
                context['recent_partner_applications'] = PartnershipApplication.objects.order_by('-created_at')[:5]

                # press_center – عام
                context['press_page_exists'] = PressCenterPage.objects.exists()
                if PressCenterPage.objects.exists():
                    context['press_page_pk'] = PressCenterPage.objects.first().pk
                context['press_images_count'] = PressCenterImage.objects.count()
                context['publication_requests_count'] = PublicationRequest.objects.count()
                context['recent_publication_requests'] = PublicationRequest.objects.order_by('-created_at')[:5]

                # PROJECTS – يمكن تصفيتها
                context['projects_count'] = Project.objects.count()
                context['project_categories_count'] = ProjectCategory.objects.count()
                context['project_members_count'] = ProjectMember.objects.count()
                context['project_partners_count'] = ProjectPartner.objects.count()
                context['project_slides_count'] = ProjectSlide.objects.count()
                context['project_gallery_count'] = ProjectGallery.objects.count()
                context['contact_requests_count'] = ContactRequest.objects.count()
                context['project_proposals_count'] = ProjectProposal.objects.count()
                context['project_join_requests_count'] = ProjectJoinRequest.objects.count()
                context['recent_proposals'] = ProjectProposal.objects.order_by('-created_at')[:5]
                context['recent_join_requests'] = ProjectJoinRequest.objects.order_by('-created_at')[:5]

                # schedule – يمكن تصفيتها
                context['schedule_programs_count'] = ScheduleProgram.objects.count()
                context['schedule_modules_count'] = CurriculumModule.objects.count()
                context['schedule_documents_count'] = CurriculumDocument.objects.count()
                context['schedule_applications_count'] = ProgramApplication.objects.count()
                context['schedule_slider_count'] = ScheduleSliderImage.objects.count()
                context['calendar_slider_count'] = CalendarSliderImage.objects.count()
                context['recent_program_applications'] = ProgramApplication.objects.order_by('-created_at')[:5]

                # RESEARCH – يمكن تصفيتها
                context['research_categories_count'] = ResearchCategory.objects.count()
                context['research_count'] = Research.objects.count()
                context['research_tags_count'] = ResearchTag.objects.count()
                context['research_hero_count'] = ResearchHero.objects.count()
                context['conferences_count'] = Conference.objects.count()
                context['conference_registrations_count'] = ConferenceRegistration.objects.count()
                context['youth_departments_count'] = YouthCouncilDepartment.objects.count()
                context['youth_members_count'] = YouthCouncilMember.objects.count()

                # SINGLE WINDOW – يمكن تصفيتها
                context['basic_info_exists'] = BasicInfo.objects.exists()
                if BasicInfo.objects.exists():
                    context['basic_info_pk'] = BasicInfo.objects.first().pk
                context['sliders_count'] = Slider.objects.count()
                context['singlewindow_faqs_count'] = SingleWindowFAQ.objects.count()
                context['service_requests_count'] = ServiceRequest.objects.count()
                context['recent_service_requests'] = ServiceRequest.objects.order_by('-created_at')[:5]

                # STAFF – يمكن تصفيتها
                context['team_members_count'] = TeamMember.objects.count()
                context['teacher_programs_count'] = TeacherProgram.objects.count()
                context['page_heroes_count'] = PageHero.objects.count()
                context['recent_team_members'] = TeamMember.objects.order_by('-created_at')[:5]

                # Patents – يمكن تصفيتها
                context['patent_images_count'] = PatentImage.objects.count()
                context['active_patent_images'] = PatentImage.objects.filter(is_active=True).count()
                context['recent_patent_images'] = PatentImage.objects.order_by('-created_at')[:5]

        return context