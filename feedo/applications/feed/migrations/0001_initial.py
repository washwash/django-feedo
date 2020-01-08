from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.URLField()),
                ('updated_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField()),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField()),
                ('guid', models.TextField(blank=True, null=True)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='feed.Feed')),
            ],
            options={
                'ordering': ('-published_at',),
            },
        ),
    ]
