from django.core.management import BaseCommand
from mailing.services import *


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        frequently_send_mailings(1)
