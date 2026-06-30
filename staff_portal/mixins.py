from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/staff/login/'

    def test_func(self):
        return self.request.user.is_staff


class StaffLoginView(LoginView):
    template_name = 'staff_portal/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/staff/'


class StaffLogoutView(LogoutView):
    next_page = '/staff/login/'
