from django.conf import settings
from django.db import models
from django.db.models import Q

from app.models import TimestampModel
from core.constants import DRIVER
from core.constants import MANAGEMENT
from core.constants import MECHANIC

from .constants import ORDER_STATUS
from .constants import REASON_TYPE
from .helpers.get_order_number import get_order_number


class Reason(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=32, unique=True)
    type = models.IntegerField(verbose_name="Тип", choices=REASON_TYPE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Причина"
        verbose_name_plural = "Причины"
        ordering = (
            "type",
            "name",
        )


class Post(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("name",)


class Order(TimestampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="orders"
    )
    number = models.IntegerField(verbose_name="Номер", unique=True)
    status = models.IntegerField(verbose_name="Статус", choices=ORDER_STATUS)
    reason = models.ForeignKey(
        Reason,
        verbose_name="Причина",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    date_begin = models.DateTimeField(verbose_name="Дата и время начала работ")
    date_end = models.DateTimeField(verbose_name="Дата и время завершения работ", blank=True, null=True)
    post = models.ForeignKey(
        Post, verbose_name="Пост", on_delete=models.PROTECT, related_name="orders", blank=True, null=True
    )
    car = models.ForeignKey(
        "core.Car", verbose_name="ТС", on_delete=models.PROTECT, related_name="orders", blank=True, null=True
    )
    driver = models.ForeignKey(
        "core.Employee",
        verbose_name="Водитель",
        on_delete=models.PROTECT,
        limit_choices_to={"type": DRIVER},
        related_name="orders_from_driver",
        blank=True,
        null=True,
    )
    responsible = models.ForeignKey(
        "core.Employee",
        verbose_name="Ответсвенный",
        on_delete=models.PROTECT,
        limit_choices_to={"type": MANAGEMENT},
        related_name="orders_from_responsible",
        blank=True,
        null=True,
    )
    odometer = models.IntegerField(verbose_name="Пробег", blank=True, null=True)
    note = models.TextField(verbose_name="Примечание", blank=True)

    def __str__(self):
        return f"{self.number} - {self.date_begin.strftime('%d.%m.%Y')} - {self.car}"

    class Meta:
        verbose_name = "Заказ-наряд"
        verbose_name_plural = "Заказ-наряды"
        ordering = ("-number",)

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = get_order_number()
        super().save(*args, **kwargs)


class WorkCategory(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория работ"
        verbose_name_plural = "Категории работ"
        ordering = ("name",)


class Work(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=64, unique=True)
    category = models.ForeignKey(
        WorkCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name="works"
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"
        ordering = ("name",)


class OrderWork(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ-наряд", on_delete=models.CASCADE, related_name="order_works")
    work = models.ForeignKey(Work, verbose_name="Работа", on_delete=models.PROTECT, related_name="order_works")
    quantity = models.IntegerField(verbose_name="Количество", default=1)
    time_minutes = models.IntegerField(verbose_name="Затрачено времени, мин", blank=True, null=True)
    note = models.TextField(verbose_name="Примечание", blank=True)

    def __str__(self):
        return f"{self.work.name} ({self.order})"

    class Meta:
        verbose_name = "Работа в заказ-наряде"
        verbose_name_plural = "Работы в заказ-наряде"


class OrderWorkMechanic(models.Model):
    order_work = models.ForeignKey(
        OrderWork, verbose_name="Работа", on_delete=models.CASCADE, related_name="mechanics"
    )
    mechanic = models.ForeignKey(
        "core.Employee",
        verbose_name="Слесарь",
        on_delete=models.PROTECT,
        limit_choices_to=Q(type=MECHANIC) | Q(type=DRIVER),
        related_name="order_works",
    )
    time_minutes = models.IntegerField(verbose_name="Затрачено времени, мин", blank=True, null=True)

    def __str__(self):
        return f"{self.mechanic.short_fio} ({self.order_work})"

    class Meta:
        verbose_name = "Работа слесарей в заказ-наряде"
        verbose_name_plural = "Работы слесарей в заказ-наряде"
