import mock
from datetime import datetime

from django.conf import settings
from django.urls import reverse

from applications.feed.tests.factories import FeedFactory
from applications.subscription.models import Subscription
from applications.subscription.tests.factories import \
    SubscriptionWithPostsFactory


HTTP_200_OK = 200
HTTP_302_REDIRECT = 302
HTTP_404_NOT_FOUND = 404


def test_subscription_create(user_logged_client, user):
    assert not Subscription.objects.count()

    url = reverse('subscription:subscription_create_view')
    data = {
        'source': 'https://dum.my/rss/'
    }

    response = user_logged_client.post(url, data)
    assert response.status_code == HTTP_302_REDIRECT
    assert response.url == reverse('subscription:subscription_list_view')
    assert Subscription.objects.count() == 1

    subscription = Subscription.objects.first()
    assert subscription.user == user
    assert subscription.feed.source == data['source']


def test_subscription_fulfill_posts(user_logged_client, user):
    feed = FeedFactory(source='https://dum.my/rss/')

    url = reverse('subscription:subscription_create_view')
    data = {
        'source': feed.source
    }

    user_logged_client.post(url, data)
    assert Subscription.objects.count() == 1
    subscription = Subscription.objects.first()

    assert subscription.posts.exists()
    assert subscription.posts.count() == feed.items.count()
    assert all(
        subscription.posts.all().values_list('is_read', flat=True)
    )


def test_subscription_list(user_logged_client, user):
    SubscriptionWithPostsFactory()
    SubscriptionWithPostsFactory(user=user)
    SubscriptionWithPostsFactory(user=user)

    url = reverse('subscription:subscription_list_view')
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_200_OK

    assert Subscription.objects.filter(user=user).count() == 2
    assert (
        set(response.context_data['object_list']) ==
        set(Subscription.objects.filter(user=user))
    )


def test_subscription_detail(user_logged_client, user):
    sub_out_of_view = SubscriptionWithPostsFactory()
    sub_in_view = SubscriptionWithPostsFactory(user=user)

    url = reverse(
        'subscription:subscription_detail_view',
        kwargs={'pk': sub_in_view.pk}
    )
    response = user_logged_client.get(url)

    assert (
        set([response.context_data['object'], ]) ==
        set(Subscription.objects.filter(user=user))
    )

    url = reverse(
        'subscription:subscription_detail_view',
        kwargs={'pk': sub_out_of_view.pk}
    )
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_subscription_delete(user_logged_client, user):
    sub_out_of_view = SubscriptionWithPostsFactory()
    sub_in_view = SubscriptionWithPostsFactory(user=user)

    detail_url = reverse(
        'subscription:subscription_detail_view',
        kwargs={'pk': sub_in_view.pk}
    )
    url = reverse(
        'subscription:subscription_delete_view',
        kwargs={'pk': sub_in_view.pk}
    )
    response = user_logged_client.post(url)
    assert response.status_code == HTTP_302_REDIRECT
    assert response.url == reverse('subscription:subscription_list_view')

    url = reverse(
        'subscription:subscription_delete_view',
        kwargs={'pk': sub_out_of_view.pk}
    )
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND

    response = user_logged_client.get(detail_url)
    assert response.status_code == HTTP_404_NOT_FOUND


@mock.patch(
    'applications.feed.service.update_feeds',
    return_value=None
)
def test_subscription_update(mock_f, user_logged_client, user):
    feed = FeedFactory(fail_count=settings.FEED_MAXIMUM_TRIES_COUNT + 1)
    subscription = SubscriptionWithPostsFactory(
        user=user,
        feed=feed,
        updated_at=datetime(1970, 1, 1)
    )
    subscription.posts.all().delete()

    url = reverse(
        'subscription:subscription_update_feed_view',
        kwargs={'pk': subscription.pk}
    )
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_302_REDIRECT
    assert (
        response.url ==
        reverse(
            'subscription:subscription_detail_view',
            kwargs={'pk': subscription.pk}
        )
    )

    assert (
        subscription.posts.exists() and
        set([p.item for p in subscription.posts.all()]) ==
        set(feed.items.all())
    )
    assert (
        set([p.is_read for p in subscription.posts.all()]) ==
        set([False, ])
    )
