from django.core.management.base import BaseCommand
from apps.core.models import receive_callback


class Command(BaseCommand):
    def handle(self, *args, **options):
        receive_callback()
