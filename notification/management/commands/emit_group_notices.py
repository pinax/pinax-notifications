import logging

from django.core.management.base import BaseCommand

from notification.engine import send__all_grouped


class Command(BaseCommand):
    help = "Emit queued group notices."

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        send__all_grouped(*args)
