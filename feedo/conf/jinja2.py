from jinja2 import Environment

from django.urls import reverse
from django.utils.timezone import template_localtime

from applications.base.jinja_register import registered_jinja_functions


def environment(**options):
    env = Environment(**options)
    env.globals.update(**registered_jinja_functions)
    env.globals.update({
        'reverse': reverse,
        'localtime': template_localtime,
    })
    return env
