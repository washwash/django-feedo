from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


class SignInView(LoginView):
    template_name = 'sign_in.html'


class SignOutView(LogoutView):
    template_name = None


class SignUpView(CreateView):
    template_name = 'sign_up.html'
    form_class = UserCreationForm

    def _sign_in(self, user):
        if user:
            login(self.request, user)

    def post(self, request, *args, **kwargs):
        result = super(SignUpView, self).post(request, *args, **kwargs)
        self._sign_in(self.object)
        return result

    @property
    def success_url(self):
        return reverse(settings.LOGIN_REDIRECT_URL)


sign_in_view = SignInView.as_view()
sign_up_view = SignUpView.as_view()
sign_out_view = SignOutView.as_view()
