from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.constants import MANAGEMENT

from .constants import TURNOVER_TYPE


class Warehouse(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ("name",)


class Unit(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=16, unique=True)
    is_precision_point = models.BooleanField(
        verbose_name="Число с плавающей запятой",
        help_text="Отметьте, если для измерения количества требуется точность с плавающей запятой.",
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ("name",)


class MaterialCategory(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория материалов"
        verbose_name_plural = "Категории материалов"
        ordering = ("name",)


class Material(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=128, unique=True)
    unit = models.ForeignKey(
        Unit, verbose_name="Единица измерения", on_delete=models.PROTECT, related_name="materials"
    )
    category = models.ForeignKey(
        MaterialCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name="materials"
    )
    article_number = models.CharField(verbose_name="Код (Артикул)", max_length=32, unique=True, null=True, blank=True)
    compatbility = ArrayField(models.CharField(max_length=64), verbose_name="Cовместимость c ТС", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ("name",)


class Entrance(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="entrances"
    )
    date = models.DateField(verbose_name="Дата")
    document_number = models.CharField(verbose_name="Номер документа", max_length=64, blank=True)
    responsible = models.ForeignKey(
        "core.Employee",
        verbose_name="Кто оприходовал",
        on_delete=models.PROTECT,
        limit_choices_to={"type": MANAGEMENT},
        related_name="enrance_from_responsible",
    )
    provider = models.CharField(verbose_name="Поставщик", max_length=128, blank=True)
    note = models.TextField(verbose_name="Примечание", blank=True)

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.provider}"

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступления"
        ordering = ("-date", "-pk")


class Turnover(models.Model):
    type = models.IntegerField(verbose_name="Тип", choices=TURNOVER_TYPE)
    date = models.DateField(verbose_name="Дата")
    is_correction = models.BooleanField(verbose_name="Корректировка", default=False)
    note = models.TextField(verbose_name="Примечание", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="turnover"
    )
    material = models.ForeignKey(Material, verbose_name="Материал", on_delete=models.PROTECT, related_name="turnovers")
    warehouse = models.ForeignKey(Warehouse, verbose_name="Склад", on_delete=models.PROTECT, related_name="turnovers")
    price = models.DecimalField(verbose_name="Цена", max_digits=12, decimal_places=2)
    quantity = models.DecimalField(verbose_name="Количество", max_digits=9, decimal_places=2)
    sum = models.DecimalField(verbose_name="Сумма", max_digits=12, decimal_places=2)
    order = models.ForeignKey(
        "orders.Order",
        verbose_name="Заказ-наряд",
        on_delete=models.PROTECT,
        related_name="turnovers_from_order",
        blank=True,
        null=True,
    )
    entrance = models.ForeignKey(
        Entrance,
        verbose_name="Приход",
        on_delete=models.PROTECT,
        related_name="turnovers_from_entrance",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.material.name} ({self.quantity})"

    class Meta:
        verbose_name = "Движение материала"
        verbose_name_plural = "Движение материалов"
        ordering = ("date", "pk")

    def save(self, *args, **kwargs):
        if self.type == 1:
            self.price = abs(self.price)
            self.quantity = abs(self.quantity)
            self.sum = abs(self.sum)
        elif self.type == 2:
            self.price = abs(self.price)
            self.quantity = -abs(self.quantity)
            self.sum = -abs(self.sum)
        super().save(*args, **kwargs)
