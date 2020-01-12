import datetime

import feedparser
import mock
import pytz

from freezegun import freeze_time
from django.conf import settings

from applications.feed.tests.entries import BASE_ENTRIES, DUPLICATE_ENTRIES
from applications.feed.models import Feed
from applications.feed.service import get_feeds_for_update, update_feeds
from applications.feed.tests.factories import FeedFactory


def test_get_feeds_for_update(db):
    assert not Feed.objects.exists()
    assert not get_feeds_for_update()

    for _ in range(3):
        FeedFactory(
            fail_count=0
        )

    for _ in range(2):
        FeedFactory(
            fail_count=settings.FEED_MAXIMUM_TRIES_COUNT
        )

    for _ in range(3):
        FeedFactory(
            fail_count=settings.FEED_MAXIMUM_TRIES_COUNT + 1
        )

    assert (
        set(Feed.objects.filter(
            fail_count__lte=settings.FEED_MAXIMUM_TRIES_COUNT
        )) ==
        set(get_feeds_for_update())
    )
    assert len(get_feeds_for_update()) == 5


def _init_mock(values):
    objects = []
    for value in values:
        obj =mock.MagicMock()
        type(obj).bozo = 0
        obj.__getitem__.side_effect = (
            lambda name: {'entries': value}[name]
        )
        objects.append(obj)
    return objects


def test_update_feeds(db):
    feed = FeedFactory(fail_count=5)
    feed.items.all().delete()

    with mock.patch.object(
        feedparser, 'parse', side_effect=_init_mock([BASE_ENTRIES, ])
    ):
        update_feeds(Feed.objects.all())

    feed.refresh_from_db()
    assert feed.items.count() == 3
    assert feed.fail_count == 0
    assert (
        set(feed.items.all().values_list('link', flat=True)) ==
        set([
            'https://li.nk/rss/1/',
            'https://li.nk/rss/2/',
            'https://li.nk/rss/3/'
        ])
    )


def test_update_feeds_updated_time(db):
    feed = FeedFactory(fail_count=settings.FEED_MAXIMUM_TRIES_COUNT + 1)
    feed.items.all().delete()

    updated_time = datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.utc)
    with mock.patch.object(
        feedparser, 'parse', side_effect=_init_mock([BASE_ENTRIES, ])
    ):
        with freeze_time(updated_time):
            update_feeds(Feed.objects.all())

    feed.refresh_from_db()
    assert feed.updated_at == updated_time


def test_update_feeds_empty(db):
    feed_empty = FeedFactory()
    feed_empty.items.all().delete()

    with mock.patch.object(
        feedparser, 'parse', side_effect=_init_mock([{}, ])
    ):
        update_feeds([feed_empty, ])

    feed_empty.refresh_from_db()
    assert not feed_empty.items.exists()


def test_update_feeds_duplicates(db):
    feed = FeedFactory()
    feed.items.all().delete()

    with mock.patch.object(
        feedparser, 'parse', side_effect=_init_mock([DUPLICATE_ENTRIES, ])
    ):
        update_feeds([feed, ])

    feed.refresh_from_db()
    assert feed.items.count() == 1


def test_update_feeds_fail(db):
    feed = FeedFactory(fail_count=0)
    feed.items.all().delete()

    fail = _init_mock([BASE_ENTRIES, ])
    type(fail[0]).bozo = 1

    with mock.patch.object(feedparser, 'parse', side_effect=fail):
        update_feeds([feed, ])

    feed.refresh_from_db()
    assert not feed.items.exists()
    assert feed.fail_count == 1
