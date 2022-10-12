from django.test import TestCase

from ..constants import EMPLOYEE_TYPE
from .factory import CarFactory
from .factory import EmployeeFactory


class CarModelTestCase(TestCase):
    def setUp(self):
        self.car = CarFactory()

    def test_fields(self):
        self.assertEqual(self.car.__str__(), "УАЗ 111 (А 777 АА)")

        gos_nom_in_putewka_unique = self.car._meta.get_field("gos_nom_in_putewka").unique
        self.assertEqual(gos_nom_in_putewka_unique, True)

        gos_nom_in_putewka_max_length = self.car._meta.get_field("gos_nom_in_putewka").max_length
        self.assertEqual(gos_nom_in_putewka_max_length, 4)

        state_number_unique = self.car._meta.get_field("state_number").unique
        self.assertEqual(state_number_unique, True)

        state_number_max_length = self.car._meta.get_field("state_number").max_length
        self.assertEqual(state_number_max_length, 16)

        name_unique = self.car._meta.get_field("name").unique
        self.assertEqual(name_unique, False)

        name_max_length = self.car._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 64)

        kod_driver_null = self.car._meta.get_field("kod_driver").null
        self.assertEqual(kod_driver_null, True)

        kod_driver_blank = self.car._meta.get_field("kod_driver").blank
        self.assertEqual(kod_driver_blank, True)

        date_decommissioned_null = self.car._meta.get_field("date_decommissioned").null
        self.assertEqual(date_decommissioned_null, True)

        date_decommissioned_blank = self.car._meta.get_field("date_decommissioned").blank
        self.assertEqual(date_decommissioned_blank, True)


class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory()

    def test_fields(self):
        self.assertEqual(self.employee.__str__(), "Иванов И. И. (Слесарь)")
        self.assertEqual(self.employee.short_fio, "Иванов И. И.")
        self.assertEqual(self.employee.type_name, "Слесарь")

        number_in_kadry_unique = self.employee._meta.get_field("number_in_kadry").unique
        self.assertEqual(number_in_kadry_unique, True)

        first_name_max_length = self.employee._meta.get_field("first_name").max_length
        self.assertEqual(first_name_max_length, 24)

        last_name_max_length = self.employee._meta.get_field("last_name").max_length
        self.assertEqual(last_name_max_length, 24)

        patronymic_blank = self.employee._meta.get_field("patronymic").blank
        self.assertEqual(patronymic_blank, True)

        patronymic_max_length = self.employee._meta.get_field("patronymic").max_length
        self.assertEqual(patronymic_max_length, 24)

        type_choices = self.employee._meta.get_field("type").choices
        self.assertEqual(type_choices, EMPLOYEE_TYPE)

        position_max_length = self.employee._meta.get_field("position").max_length
        self.assertEqual(position_max_length, 32)

        date_dismissal_null = self.employee._meta.get_field("date_dismissal").null
        self.assertEqual(date_dismissal_null, True)

        date_dismissal_blank = self.employee._meta.get_field("date_dismissal").blank
        self.assertEqual(date_dismissal_blank, True)
