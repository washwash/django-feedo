from datetime import datetime
from factory.fuzzy import FuzzyDate
from factory import post_generation, SubFactory, Faker
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model

from applications.subscription.models import Subscription, Post


class SubscriptionFactory(DjangoModelFactory):
    feed = SubFactory(
        'applications.feed.tests.factories.FeedFactory'
    )
    user = SubFactory(
        'applications.subscription.tests.factories.UserFactory'
    )

    class Meta:
        model = Subscription


class SubscriptionWithPostsFactory(SubscriptionFactory):
    updated_at = FuzzyDate(
        datetime.utcnow().date()
    )

    @post_generation
    def create_items(obj, create, *args, **kwargs):
        if not create:
            return

        for item in obj.feed.items.all():
            PostFactory(
                subscription=obj,
                item=item,
                user=obj.user
            )


class PostFactory(DjangoModelFactory):
    user = SubFactory(
        'applications.subscription.tests.factories.UserFactory'
    )
    subscription = SubFactory(
        'applications.subscription.tests.factories.SubscriptionFactory'
    )
    item = SubFactory(
        'applications.feed.tests.factories.ItemFactory'
    )

    class Meta:
        model = Post


class UserFactory(DjangoModelFactory):
    username = Faker('name')

    class Meta:
        model = get_user_model()
