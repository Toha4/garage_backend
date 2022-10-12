from django.core.management.base import BaseCommand

from core.helpers.syncing_employees import SyncingEmployees


class Command(BaseCommand):
    """Команда для синхронизации работников из программы Кадры"""

    def handle(self, *args, **options):
        SyncingEmployees(self.stdout).sync()
