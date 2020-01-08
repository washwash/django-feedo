from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):

    @property
    def template_name(self):
        return 'index_sign_up.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('subscription:post_list_view'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)


index = IndexView.as_view()
