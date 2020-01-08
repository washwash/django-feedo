from django.apps import AppConfig


class Config(AppConfig):
    name = 'applications.subscription'

    def ready(self):
        super(Config, self).ready()
        from .templatetags import extras
