from datetime import datetime

from factory import post_generation, Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDate, FuzzyInteger

from applications.feed.models import Feed, Item


class ItemFactory(DjangoModelFactory):
    published_at = FuzzyDate(
        datetime.utcnow().date()
    )
    feed = SubFactory(
        'applications.feed.tests.factories.FeedFactory'
    )

    class Meta:
        model = Item


class FeedFactory(DjangoModelFactory):
    source = Faker('url')
    fail_count = FuzzyInteger(low=0)

    @post_generation
    def create_items(obj, create, *args, **kwargs):
        if not create:
            return

        for _ in range(3):
            ItemFactory(feed=obj)

    class Meta:
        model = Feed
