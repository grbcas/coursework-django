from django.core.management import BaseCommand
from mailing.services import get_client_emails_list


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        get_client_emails_list()
