import logging
import feedparser

from dateutil import parser
from django.conf import settings
from django.utils import timezone

from applications.feed.models import Item, Feed


logger = logging.getLogger(__name__)


def get_feeds_for_update():
    return Feed.objects.filter(
        fail_count__lte=settings.FEED_MAXIMUM_TRIES_COUNT
    )


def update_feeds(feeds):
    if not isinstance(feeds, type(Feed.objects)):
        feeds = Feed.objects.filter(pk__in=[f.pk for f in feeds])

    for feed in feeds:
        parsed = feedparser.parse(feed.source)
        if parsed.bozo and parsed.bozo_exception:
            feed.fail_count += 1
            logger.warning(
                f'{feed} got {feed.fail_count} update fails. '
                f'Reason: {parsed.bozo_exception}'
            )
        else:
            feed.fail_count = 0
            for entry in parsed['entries']:
                published_at = parser.parse(entry['published'])
                Item.objects.get_or_create(
                    defaults={
                        'title': entry['title'],
                        'link': entry['link'],
                        'description': entry['summary'],
                        'published_at': published_at
                    },
                    guid=entry['guid'],
                    feed=feed,
                )

        feed.updated_at = timezone.now()
        feed.save()
