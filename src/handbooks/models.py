from django.db import models

from .constants import EMPLOYEE_TYPE
from .constants import REASON_TYPE


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


class Car(models.Model):
    kod_mar_in_putewka = models.IntegerField(verbose_name="Номер в программе Путевки")
    gos_nom_in_putewka = models.CharField(
        verbose_name="Гос. номер в программе Путевки (PK)", max_length=4, unique=True
    )
    state_number = models.CharField(verbose_name="Гос. номер", max_length=16, unique=True)
    name = models.CharField(verbose_name="Наименование", max_length=64)
    kod_driver = models.IntegerField(verbose_name="Код водителя в программе Путевки", null=True, blank=True)
    date_decommissioned = models.DateField(verbose_name="Дата списания", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.state_number})"

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"
        ordering = (
            "name",
            "state_number",
        )


class Employee(models.Model):
    number_in_kadry = models.IntegerField(verbose_name="Номер в программе Кадры", unique=True)
    first_name = models.CharField(verbose_name="Имя", max_length=24)
    last_name = models.CharField(verbose_name="Фамилия", max_length=24)
    patronymic = models.CharField(verbose_name="Отчество", max_length=24, blank=True)
    type = models.IntegerField(verbose_name="Тип", choices=EMPLOYEE_TYPE)
    position = models.CharField(verbose_name="Должность", max_length=32)
    date_dismissal = models.DateField(verbose_name="Дата увольнения", null=True, blank=True)

    @property
    def short_fio(self):
        return f"{self.last_name} {self.first_name[0]}. {self.patronymic[0]}."

    @property
    def type_name(self):
        return dict((x, y) for x, y in EMPLOYEE_TYPE).get(self.type)

    def __str__(self):
        return f"{self.short_fio} ({self.type_name})"

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        ordering = (
            "type",
            "last_name",
        )
