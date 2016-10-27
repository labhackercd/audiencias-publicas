from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Schedule.objects.get(name='import-live-videos').delete()
            print('Unscheduled import-live-videos.')
        except Schedule.DoesNotExist:
            schedule('apps.core.views.receive_callback',
                     name='import-live-videos', schedule_type='I')
            print('Scheduled import-live-videos.')
