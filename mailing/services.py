from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, Client, Log


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


def toggle_state(frequency) -> None:
    """
    Функция проверки время старта/конца рассылки относительно текущего времени - меняет статус рассылки
    ---можно заменить встроенным функционалом apscheduler---
    """
    datetime_now = timezone.now()
    # mailing_list = Mailing.objects.filter(frequency=frequency) # Ошибки
    mailing_list = list(Mailing.objects.filter(frequency=frequency))

    for mailing in mailing_list:
        # print(mailing)
        mailing_dict = mailing.__dict__
        start_time = mailing_dict.get('start_time')
        stop_time = mailing_dict.get('stop_time')
        status_stop = mailing_dict.get('status_stop')

        # start_time = mailing.values_list('start_time', flat=True)[0] # TypeError: 'Mailing' object is not iterable
        # stop_time = mailing.values_list('stop_time', flat=True)[0]

        if status_stop:
            continue

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
    """
    Функция отправки сообщения клиентам с частой frequency
    """
    toggle_state(frequency)

    # mailing_list = Mailing.objects.filter(frequency=frequency).filter(status_run=1) # не итерируется, нет данных из связанных таблиц

    mailing_list_id = Mailing.objects.values_list('id', flat=True).filter(frequency=frequency).filter(status_run=1)

    for pk in mailing_list_id:
        # mailing_dict = mailing.__dict__
        # print(mailing_dict)

        # emails = list(mailing.values_list('recipients__email', flat=True)) # AttributeError: 'Mailing' object has no attribute 'values_list'
        # subject = mailing.values_list('message__subject', flat=True)[0]
        # message = mailing.values_list('message__body', flat=True)[0]

        emails = list(Mailing.objects.values_list('recipients__email', flat=True).filter(pk=pk))
        subject = Mailing.objects.values_list('message__subject', flat=True).filter(pk=pk)[0]
        message = Mailing.objects.values_list('message__body', flat=True).filter(pk=pk)[0]

        print(emails, '\nsubject: ', subject, '\nmessage: ', message)

        try:
            send_mailing = send_mail(
                subject=f'{subject}',
                message=f'{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails
                )
            if send_mailing:
                status = Log.STATE[0][0]
            else:
                status = Log.STATE[1][0]

        except Exception:
            status = Log.STATE[1][0]

        print(
            '---Mailing.objects.filter(pk=pk)---',
            type(Mailing.objects.filter(pk=pk)),
              Mailing.objects
        )

        Log.objects.create(
            last_try=timezone.now(),
            status=status,
            mailing=Mailing.objects.filter(pk=pk)[0]

        )

        print(Log.__dict__)
