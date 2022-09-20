from django.core.management.base import BaseCommand

from core.helpers.syncing_cars import SyncingCars


class Command(BaseCommand):
    """Команда для синхронизации ТС из программы Путевки"""

    def handle(self, *args, **options):
        SyncingCars(self.stdout).sync()
