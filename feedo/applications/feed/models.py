import uuid

from django.db import models


class Feed(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    source = models.URLField(
    )
    updated_at = models.DateTimeField(
        null=True
    )


class Item(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name='items'
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )
    published_at = models.DateTimeField(
    )
    title = models.TextField(
        null=False,
        blank=False
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    link = models.URLField(
        null=False,
        blank=False
    )
    guid = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-published_at', )
