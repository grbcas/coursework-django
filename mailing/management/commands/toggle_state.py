from django.core.management import BaseCommand
from mailing.services import toggle_state


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        toggle_state(1)
