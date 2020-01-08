from applications.base import jinja_register as register
from applications.subscription.service import get_unread_count


@register.function
def unread_count(user, subscription=None):
    return get_unread_count(user, subscription)
