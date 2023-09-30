from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, Client
from users.models import User


def send_mailing(mailing: Mailing, client: Client):

    message = mailing.message
    send_mail(
        subject='Верификация почты',
        message=f'{message}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client.email]
    )
