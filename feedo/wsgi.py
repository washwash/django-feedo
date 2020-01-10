import os

import configurations
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

configurations.setup()
application = get_wsgi_application()
