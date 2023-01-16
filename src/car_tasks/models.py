from django.conf import settings
from django.db import models

from app.models import TimestampModel


class CarTask(TimestampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="tasks"
    )
    car = models.ForeignKey("core.Car", verbose_name="ТС", on_delete=models.PROTECT, related_name="tasks")
    description = models.TextField(verbose_name="Описание", blank=True)
    materials = models.TextField(verbose_name="Необходимые материалы", blank=True)
    is_completed = models.BooleanField(verbose_name="Выполнен", default=False)
    date_completed = models.DateField(verbose_name="Дата выполнения", blank=True, null=True)
    order = models.ForeignKey(
        "orders.Order",
        verbose_name="Заказ-наряд",
        on_delete=models.PROTECT,
        related_name="tasks_from_order",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.car.name} - {self.description} ({self.created.strftime('%d.%m.%Y')})"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ("-created", "pk")
