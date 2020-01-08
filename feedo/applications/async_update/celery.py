import os
import configurations
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
configurations.setup()

app = Celery('Feedo')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
