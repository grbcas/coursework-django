from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, Client, Message
from users.models import User


def get_user_statistic(user) -> dict:
    """
    Получение статистики юзера для вывода на home.html

    """

    user_statistic = {
        'total_mailings': Mailing.objects.filter(owner=user).count(),
        'active_mailings': Mailing.objects.filter(owner=user).filter(status_run=1).count(),
        'clients': Mailing.objects.values_list('recipients__email', flat=True).filter(owner=user).count()
    }

    return user_statistic


def manual_send_mailing(pk):
    """
    Функция отправки сообщения клиентам рассылки кнопкой Send.
    """

    mailing_list = list(Mailing.objects.values_list('recipients__email', flat=True).filter(pk=pk))
    subject = Mailing.objects.values_list('message__subject', flat=True).filter(pk=pk)[0]
    message = Mailing.objects.values_list('message__body', flat=True).filter(pk=pk)[0]
    print(mailing_list)
    send_mail(
        subject=f'{subject}',
        message=f'{message}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=mailing_list
    )


def toggle_state() -> None:
    """
    Функция проверки время старта/конца рассылки относительно текущего времени - меняет статус рассылки
    ---можно заменить встроенным функционалом apscheduler---
    """
    datetime_now = timezone.now()
    mailing_list = Mailing.objects.filter(frequency=frequency)
    for mailing in mailing_list:
        start_time = mailing.values_list('start_time', flat=True)[0] # datetime.datetime(2023, 10, 3, 15, 19, tzinfo=datetime.timezone.utc)
        stop_time = mailing.values_list('stop_time', flat=True)[0]
        if not stop_time:
            if datetime_now > start_time:
                mailing.status_run = 1
        else:
            if datetime_now < stop_time:
                mailing.status_run = 1
            else:
                mailing.status_run = 0
                mailing.status_stop = 1
        mailing.save()


def frequently_send_mailings(frequency):
    toggle_state()
    mailing_list = Mailing.objects.filter(frequency=frequency).filter(status_run=1)

    for mailing in mailing_list:
        emails = list(mailing.values_list('recipients__email', flat=True))
        subject = mailing.values_list('message__subject', flat=True)[0]
        message = mailing.values_list('message__body', flat=True)[0]
        print(emails, '/n', subject, '/n', message)

        send_mail(
            subject=f'{subject}',
            message=f'{message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=mailing_list
        )
