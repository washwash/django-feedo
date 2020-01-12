from applications.base import jinja_register as register
from applications.subscription.service import get_unread_count
from django.conf import settings


@register.function
def unread_count(user, subscription=None):
    return get_unread_count(user, subscription)


@register.function
def is_subscription_active(subscription):
    return subscription.feed.fail_count <= settings.FEED_MAXIMUM_TRIES_COUNT
