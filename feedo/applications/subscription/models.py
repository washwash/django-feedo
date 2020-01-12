import uuid

from django.db import models

from applications.base.model_mixins import UserTenantModel
from applications.feed.models import Feed, Item


class Subscription(UserTenantModel, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    feed = models.ForeignKey(
        Feed,
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        null=True
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('-subscribed_at', )
        unique_together = (
            ('user', 'feed'),
        )


class Post(UserTenantModel, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    is_read = models.BooleanField(
        default=False
    )
    is_favourite = models.BooleanField(
        default=False
    )
    comment = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-item__published_at', )
