from copy import copy

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from applications.authentication.filters import UserTenantFilterBackend
from applications.base.views_mixins import FilterBackendViewMixin
from applications.feed.service import update_feeds
from applications.subscription.forms import (
    SubscriptionCreationForm,
    PostUpdateForm
)
from applications.subscription.models import Subscription, Post
from applications.subscription.service import (
    update_subscriptions,
    mark_as_read,
    bind_new_posts
)


class BaseSubscriptionUserTenantView(FilterBackendViewMixin):
    model = Subscription
    queryset = (
        model.objects.
        select_related('feed').
        prefetch_related('posts')
    )
    filter_backends = [UserTenantFilterBackend, ]


class BasePostUserTenantView(FilterBackendViewMixin):
    model = Post
    queryset = (
        model.objects.
        select_related('item', 'subscription')
    )
    filter_backends = [UserTenantFilterBackend, ]


class SubscriptionsListView(BaseSubscriptionUserTenantView, ListView):
    template_name = 'subscription_list.html'


class SubscriptionsDetailView(BaseSubscriptionUserTenantView, DetailView):
    template_name = 'subscription_detail.html'


class SubscriptionsUpdateFeedView(SubscriptionsDetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        update_feeds([self.object.feed, ])
        update_subscriptions([self.object, ])
        self.object.refresh_from_db()

        detail_url = reverse(
            'subscription:subscription_detail_view',
            kwargs={'pk': self.object.pk}
        )
        return redirect(detail_url)


class SubscriptionsCreateView(CreateView):
    template_name = 'subscription_form.html'
    form_class = SubscriptionCreationForm

    def get_form_kwargs(self):
        kwargs = super(SubscriptionsCreateView, self).get_form_kwargs()

        if kwargs.get('data'):
            base_data = copy(kwargs['data'])
            base_data['user'] = self.request.user.pk
            kwargs['data'] = base_data
        return kwargs

    def get_success_url(self):
        return reverse('subscription:subscription_list_view')

    def form_valid(self, form):
        result = super(SubscriptionsCreateView, self).form_valid(form)
        bind_new_posts(self.object)
        mark_as_read(self.object.posts.all())
        return result


class SubscriptionsDeleteView(BaseSubscriptionUserTenantView, DeleteView):
    template_name = 'subscription_confirm_delete.html'

    def get_success_url(self):
        return reverse('subscription:subscription_list_view')


class PostUpdateView(BasePostUserTenantView, UpdateView):
    template_name = 'post_detail.html'
    form_class = PostUpdateForm

    def get(self, request, *args, **kwargs):
        result = super(PostUpdateView, self).get(request, *args, **kwargs)
        mark_as_read([self.object, ])
        return result

    def get_success_url(self):
        return reverse(
            'subscription:post_detail_view',
            kwargs={
                'pk': self.object.pk
            }
        )


class PostListView(BasePostUserTenantView, ListView):
    paginate_by = 10
    template_name = 'post_list.html'


class PostFavouritesView(PostListView):
    template_name = 'post_favourites.html'

    def get_queryset(self):
        queryset = super(PostFavouritesView, self).get_queryset()
        return queryset.filter(is_favourite=True)


class PostListNewView(PostListView):
    template_name = 'post_list_new.html'

    def get_queryset(self):
        queryset = super(PostListNewView, self).get_queryset()
        return queryset.filter(is_read=False)


subscriptions_list = SubscriptionsListView.as_view()
subscriptions_detail = SubscriptionsDetailView.as_view()
subscriptions_update_feed = SubscriptionsUpdateFeedView.as_view()
subscriptions_create = SubscriptionsCreateView.as_view()
subscriptions_delete = SubscriptionsDeleteView.as_view()

post_detail = PostUpdateView.as_view()
post_update = PostUpdateView.as_view()
post_list = PostListView.as_view()
post_list_new = PostListNewView.as_view()
post_favourites = PostFavouritesView.as_view()
