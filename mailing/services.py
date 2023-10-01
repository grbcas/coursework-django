from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, Client
from users.models import User


def send_mailing(mailing: Mailing, client: Client):

    message = mailing.message
    send_mail(
        subject='mailing.message',
        message=f'{message}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client.email]
    )


def get_user_statistic(user: User) -> dict:
    """
    Функция для кеширования загружаемой информации,
    которая используется в карточке статистики юзера на домашней странице
    """

    mailings = user.mailing_set.all()
    user_statistic = {
        'total_mailings': len(mailings),
        'active_mailings': len(mailings.filter(status=Mailing.status_run)),
        'clients': len(user.client_set.values('email').distinct())
    }

    return user_statistic
