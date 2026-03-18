# dashboards/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from main.models import Application

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
        # بيانات مشتركة
        context['total_applications'] = Application.objects.count()
        context['pending_applications'] = Application.objects.filter(status='pending').count()
        context['recent_applications'] = Application.objects.order_by('-created_at')[:5]

        # يمكن إضافة بيانات خاصة بكل دور هنا
        user = self.request.user
        if hasattr(user, 'profile'):
            user_type = user.profile.user_type
            if user_type == 'company' and user.profile.company:
                context['company'] = user.profile.company
            # أضف المزيد حسب الحاجة
        return context