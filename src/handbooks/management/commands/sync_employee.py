from django.core.management.base import BaseCommand

from handbooks.helpers.syncing_employee import SyncingEmployee


class Command(BaseCommand):
    """Команда для синхронизации работников из программы Кадры"""

    def handle(self, *args, **options):
        SyncingEmployee(self.stdout).sync()
