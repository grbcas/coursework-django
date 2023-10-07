from django import template
from django.db import models
from config import settings
from mailing.models import Client

register = template.Library()


@register.simple_tag
def get_user_emails(object: models.Model) -> str:
    # user_emails = object.__str__
    # print(object.recipients)
    return f'{object}'


@register.filter
def last_name(object):
    if isinstance(object, Client):
        return object.name.split()[0]


@register.filter
def first_name(object):
    if isinstance(object, Client):
        return object.name.split()[1]


@register.filter
def father_name(object):
    if isinstance(object, Client):
        name = object.name.split()
        if len(name) == 3:
            return name[2]