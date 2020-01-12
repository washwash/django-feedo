import datetime
import pytz

from django.conf import settings
from freezegun import freeze_time

from applications.subscription.templatetags.extras import (
    is_subscription_active,
    unread_count
)
from applications.feed.tests.factories import FeedFactory, ItemFactory
from applications.subscription.models import Subscription, Post
from applications.subscription.service import (
    get_subscriptions_for_update,
    get_unread_count,
    mark_as_read,
    bind_new_posts,
    update_subscriptions
)
from applications.subscription.tests.factories import (
    SubscriptionFactory,
    PostFactory,
    SubscriptionWithPostsFactory
)


def test_get_subscriptions_for_update(db):
    assert not Subscription.objects.exists()
    assert not get_subscriptions_for_update()

    for _ in range(3):
        SubscriptionFactory()

    assert (
        set(Subscription.objects.all()) ==
        set(get_subscriptions_for_update())
    )


def test_update_subscriptions(db):
    feed = FeedFactory()
    subscription = SubscriptionFactory(
        feed=feed,
        updated_at=None
    )
    assert not subscription.updated_at
    assert not subscription.posts.exists()

    updated_time = datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.utc)
    with freeze_time(updated_time):
        update_subscriptions([subscription, ])
    subscription.refresh_from_db()

    assert subscription.posts.count() == feed.items.count()
    assert (
        set(p.item for p in subscription.posts.all()) ==
        set(feed.items.all())
    )
    assert subscription.updated_at == updated_time


def test_bind_new_posts_fresh(db):
    feed = FeedFactory()
    subscription = SubscriptionFactory(
        feed=feed,
        updated_at=None
    )
    assert feed.items.exists()
    assert not subscription.updated_at
    assert not subscription.posts.exists()

    bind_new_posts(subscription)
    subscription.refresh_from_db()

    assert subscription.posts.count() == feed.items.count()
    assert (
        set(p.item for p in subscription.posts.all()) ==
        set(feed.items.all())
    )


def test_bind_new_posts_has_been_updated(user):
    created_time = datetime.datetime(2018, 1, 1, 0, 0)
    subscription = SubscriptionWithPostsFactory(
        updated_at=created_time,
        user=user
    )

    assert subscription.updated_at == created_time
    assert subscription.posts.exists()

    posts_count = subscription.posts.count()
    for _ in range(5):
        ItemFactory(feed=subscription.feed)

    bind_new_posts(subscription)
    subscription.refresh_from_db()

    assert subscription.posts.count() == posts_count + 5


def test_mark_as_read(db):
    for _ in range(2):
        PostFactory(is_read=True)

    for _ in range(5):
        PostFactory(is_read=False)
    mark_as_read(Post.objects.all())
    assert all(Post.objects.all().values_list('is_read', flat=True))

    posts = []
    for _ in range(2):
        posts.append(PostFactory(is_read=False))
    mark_as_read(posts)
    assert all(Post.objects.all().values_list('is_read', flat=True))


def test_get_unread_count(user):
    for _ in range(2):
        PostFactory(is_read=False)
    assert get_unread_count(user) == 0
    assert unread_count(user) == 0

    for _ in range(2):
        PostFactory(user=user, is_read=True)
    assert get_unread_count(user) == 0
    assert unread_count(user) == 0

    for _ in range(3):
        PostFactory(user=user, is_read=False)
    assert get_unread_count(user) == 3
    assert unread_count(user) == 3

    subscription = SubscriptionFactory()
    PostFactory(user=user, is_read=False, subscription=subscription)
    assert get_unread_count(user, subscription) == 1
    assert unread_count(user, subscription) == 1


def test_is_subscription_active(db):
    feed = FeedFactory(fail_count=settings.FEED_MAXIMUM_TRIES_COUNT - 1)
    subscription = SubscriptionFactory(
        feed=feed
    )
    assert is_subscription_active(subscription)

    feed = FeedFactory(fail_count=settings.FEED_MAXIMUM_TRIES_COUNT)
    subscription = SubscriptionFactory(
        feed=feed
    )
    assert is_subscription_active(subscription)

    feed = FeedFactory(fail_count=settings.FEED_MAXIMUM_TRIES_COUNT + 1)
    subscription = SubscriptionFactory(
        feed=feed
    )
    assert not is_subscription_active(subscription)
