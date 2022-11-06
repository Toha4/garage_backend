from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "warehouse"
    verbose_name = "Склад"
    verbose_name_plural = "Склад"

    def ready(self):
        from warehouse import receivers
