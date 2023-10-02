from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from mailing.models import Mailing, Client, Message
from users.models import User


def get_client_emails_list():
    """
    Возвращает список email клиентов рассылки
    """
    queryset_client_email = list(Client.objects.values('email').
                                 filter(status=Mailing.STATE[0][0])) # add filter for active
    clients_emails = []
    for key in queryset_client_email:
        clients_emails.append(key['email'])
    print(clients_emails)
    return clients_emails


def send_mailing():
    """
    Функция отправки сообщения клиентам рассылки.
    """

    datetime_now = timezone.now()

    mailing_list = get_client_emails_list()
    print(Mailing.objects.values('message'))
    send_mail(
        subject='mailing.message',
        message=f'mailing.message',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=mailing_list
    )


def get_user_statistic() -> dict:
    """
    Получение статистики юзера для домашней страницы
    """

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        user_clients = Client.objects.filter(owner=self.request.user)

        return context

    mailings = user.mailing_set.all()
    user_statistic = {
        'total_mailings': len(mailings),
        'active_mailings': len(mailings.filter(Mailing.status_run)),
        'clients': len(user.client_set.values('email').distinct()) # ????
    }

    return user_statistic
