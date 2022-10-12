from factory.django import DjangoModelFactory

from ..models import Car
from ..models import Employee


class CarFactory(DjangoModelFactory):
    kod_mar_in_putewka = 1
    gos_nom_in_putewka = "777"
    state_number = "А 777 АА"
    name = "УАЗ 111"
    kod_driver = 11
    date_decommissioned = None

    class Meta:
        model = Car


class EmployeeFactory(DjangoModelFactory):
    number_in_kadry = 1
    first_name = "Иван"
    last_name = "Иванов"
    patronymic = "Иванович"
    type = 2
    position = "Слесарь 1 раз."
    date_dismissal = None

    class Meta:
        model = Employee
