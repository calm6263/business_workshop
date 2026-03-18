# accounts/views.py
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class CustomLoginView(LoginView):
    template_name = 'registration/custom_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # All users go to their dashboard
        return reverse_lazy('dashboards:dashboard')

def logout_view(request):
    logout(request)
    return redirect('index')

@method_decorator(never_cache, name='dispatch')
class PersonalCabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/personal_cabinet.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_type'] = user.profile.user_type if hasattr(user, 'profile') else 'regular'
        return context