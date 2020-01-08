from dateutil import parser

from django.utils import timezone
import feedparser

from applications.feed.models import Item


def update_feed(feed):
    parsed = feedparser.parse(feed.source)

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
