import datetime

from users.models import User
from django.db import models
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):

    email = models.EmailField(unique=True, verbose_name='email address')
    comment = models.TextField(max_length=100, **NULLABLE)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Mailing(models.Model):
    """"""
    name = models.CharField(max_length=50, verbose_name='name')
    mailing_frequency = models.PositiveSmallIntegerField(default=1, verbose_name='mailing_frequency')
    mailing_time = models.TimeField(default=datetime.time(16, 00), verbose_name='mailing_time')
    status_stop = models.BooleanField(default=False, verbose_name='status_stop')
    status_run = models.BooleanField(default=False, verbose_name='status_run')
    status_set = models.BooleanField(default=True, verbose_name='status_set')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='start_time')
    end_time = models.DateTimeField(verbose_name='end_time', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)
    creation_date = models.DateTimeField(default=timezone.now, verbose_name='creation_date')
    recipients = models.ManyToManyField(Client)
    message = models.TextField(max_length=1000, verbose_name='message', **NULLABLE)

    def __str__(self):
        return f"{self.name} {self.mailing_frequency}"

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ['name']
