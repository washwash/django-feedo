from django.utils import timezone

from applications.feed.service import update_feed
from applications.subscription.models import Post, Subscription


def update_subscriptions(subscriptions):
    if not isinstance(subscriptions, type(Subscription.objects)):
        subscriptions = Subscription.objects.filter(
            pk__in=[s.pk for s in subscriptions]
        ).select_related('feed')

    for feed in set(s.feed for s in subscriptions):
        update_feed(feed)

    for subscription in subscriptions:
        bind_new_posts(subscription)

    subscriptions.update(
        updated_at=timezone.now()
    )


def bind_new_posts(subscription):
    if subscription.updated_at:
        item_for_save = subscription.feed.items.filter(
            added_at__gt=subscription.updated_at
        )
    else:
        item_for_save = subscription.feed.items.all()

    for item in item_for_save:
        Post.objects.get_or_create(
            item=item,
            subscription=subscription,
            user=subscription.user
        )


def mark_as_read(posts):
    if not isinstance(posts, type(Post.objects)):
        posts = Post.objects.filter(pk__in=[p.pk for p in posts])

    unread_posts = posts.filter(is_read=False)
    if unread_posts:
        unread_posts.update(is_read=True)

    return unread_posts


def get_unread_count(user, subscription=None):
    lookups = {
        'user': user,
        'is_read': False
    }
    if subscription:
        lookups['subscription'] = subscription

    return Post.objects.filter(**lookups).count()
