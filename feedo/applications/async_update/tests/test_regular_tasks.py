import mock
import feedparser

from django.conf import settings

from applications.async_update.tasks import update_subscriptions_task
from applications.feed.tests.factories import FeedFactory
from applications.subscription.tests.factories import SubscriptionFactory


def _init_mock():
    obj =mock.MagicMock()
    type(obj).bozo = 0
    obj.__getitem__.side_effect = (
        lambda name: [{
            'published': '12 Jan 2020 18:31:56 +0100',
            'title': 'TITLE',
            'link': 'https://li.nk/rss/1/',
            'summary': 'SUMMARY',
            'guid': 'https://li.nk/rss/1/',
        }]
    )
    return obj


def test_update_subscriptions_task_feeds(db):
    feed = FeedFactory(fail_count=0)
    feed_items_count = feed.items.count()
    feed_inactive = FeedFactory(
        fail_count=settings.FEED_MAXIMUM_TRIES_COUNT + 1
    )
    feed_inactive.items.all().delete()

    with mock.patch.object(
        feedparser, 'parse', side_effect=[_init_mock(), _init_mock()]
    ):
        update_subscriptions_task()

    feed.refresh_from_db()
    feed_inactive.refresh_from_db()

    assert feed.items.count() == feed_items_count + 1
    assert not feed_inactive.items.exists()


def test_update_subscriptions_task_subscription(db):
    subscription = SubscriptionFactory(
        updated_at=None
    )
    subscription.feed.items.all().delete()
    assert not subscription.posts.exists()

    with mock.patch.object(
        feedparser, 'parse', side_effect=[_init_mock(), _init_mock()]
    ):
        update_subscriptions_task()

    subscription.refresh_from_db()
    assert subscription.posts.count() == 1
    assert subscription.updated_at
