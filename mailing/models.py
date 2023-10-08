import datetime

from users.models import User
from django.db import models
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):

    email = models.EmailField(unique=True, verbose_name='email address')
    comment = models.TextField(max_length=100, **NULLABLE)
    name = models.CharField(max_length=150, verbose_name='ФИО',**NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    """Модель для сообщения конкретной рассылки"""

    subject = models.CharField(default='No subject', max_length=100, verbose_name='Тема')
    body = models.TextField(verbose_name='Тело письма', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Owner', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Mailing(models.Model):
    """
    Модель описания рассылки
    """
    STATE = (
        ('created', 'создана'),
        ('started', 'запущена'),
        ('finished', 'завершена')
    )

    name = models.CharField(max_length=50, verbose_name='name')
    frequency = models.PositiveSmallIntegerField(default=1, verbose_name='mailing_frequency')
    mailing_time = models.TimeField(default=datetime.time(16, 00), verbose_name='mailing_time')
    status_stop = models.BooleanField(default=False, verbose_name='status_stop')
    status_run = models.BooleanField(default=False, verbose_name='status_run')
    status_set = models.BooleanField(default=True, verbose_name='status_set')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='start_time')
    end_time = models.DateTimeField(verbose_name='end_time', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Owner', **NULLABLE)
    creation_date = models.DateTimeField(default=timezone.now, verbose_name='creation_date')
    recipients = models.ManyToManyField(Client, verbose_name='Clients', **NULLABLE)
    # message = models.TextField(max_length=1000, verbose_name='message', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение',  **NULLABLE)

    def __str__(self):
        return f"name:{self.name}, frequency: {self.frequency}, start_time:{self.start_time}"

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ['pk']


class Log(models.Model):
    """
    Модель лога рассылки
    """

    STATE = (
        ('success', 'успех'),
        ('error', 'ошибка')
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATE, verbose_name='Статус попытки')
    server_response = models.CharField(null=True, blank=True, max_length=3, verbose_name='Ответ сервера')

    # client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.last_try}: {self.server_response}, {self.status}'

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
