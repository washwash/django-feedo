from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):

    def _is_url_allowed(self, url):
        return (
            resolve(url).view_name in
            settings.IGNORE_AUTHENTICATION_REQUIRED_VIEWS
        )

    def process_request(self, request):
        if request.user.is_authenticated:
            return

        if self._is_url_allowed(request.path):
            return

        return redirect_to_login(
            next=request.path,
            login_url=resolve_url(settings.LOGIN_URL)
        )
