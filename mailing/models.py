import datetime

from django.db import models


# Create your models here.
class Mailing(models.Model):
    mailing_frequency = models.PositiveSmallIntegerField(default=1, verbose_name='mailing_frequency')
    mailing_time = models.TimeField(default=datetime.time(16, 00), verbose_name='mailing_time')
    mailing_status_stop = models.BooleanField(default=False, verbose_name='mailing stopped')
    mailing_status_run = models.BooleanField(default=False, verbose_name='mailing started')
    mailing_status_set = models.BooleanField(default=False, verbose_name='mailing created')
