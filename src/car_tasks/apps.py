from django.apps import AppConfig


class CarTasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_tasks"
    verbose_name = "Задача для ТС"
    verbose_name_plural = "Задачи для ТС"
