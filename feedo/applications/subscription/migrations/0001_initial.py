import uuid

import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feed', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='feed.Feed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-subscribed_at',),
                'unique_together': {('user', 'feed')},
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_read', models.BooleanField(default=False)),
                ('is_favourite', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='feed.Item')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='subscription.Subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-item__published_at',),
            },
        ),
    ]
