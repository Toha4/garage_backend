from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
    verbose_name = "Заказ-наряд"
    verbose_name_plural = "Заказ-наряды"
