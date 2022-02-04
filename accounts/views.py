from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserRegistration


# Create your views here.


class SignInView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index_view')


class SignUpView(CreateView, SuccessMessageMixin):
    template_name = 'register.html'
    form_class = UserRegistration
    success_url = reverse_lazy('signIn')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_pass.html'
    success_url = reverse_lazy('password_change_done')


class CustomPasswordChangedDone(PasswordChangeDoneView):
    template_name = 'password_changed.html'


class CustomPasswordReset(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('reset_done')


class CustomPasswordDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


class SignOut(LogoutView):
    next_page = 'index_view'
