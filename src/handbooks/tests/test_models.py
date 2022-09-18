from django.test import TestCase

from ..constants import EMPLOYEE_TYPE
from ..constants import REASON_TYPE
from ..models import Car
from ..models import Employee
from ..models import Post
from ..models import Reason


class ReasonModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Reason.objects.create(name="ТО", type=1)

    def test_fields(self):
        reason = Reason.objects.first()

        name_unique = reason._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = reason._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)

        type_choices = reason._meta.get_field("type").choices
        self.assertEqual(type_choices, REASON_TYPE)


class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Post.objects.create(name="Бокс 1")

    def test_fields(self):
        post = Post.objects.first()

        name_unique = post._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = post._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 16)


class CarModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )

    def test_fields(self):
        car = Car.objects.first()

        self.assertEqual(car.__str__(), "УАЗ 123 (А 777 АА)")

        gos_nom_in_putewka_unique = car._meta.get_field("gos_nom_in_putewka").unique
        self.assertEqual(gos_nom_in_putewka_unique, True)

        gos_nom_in_putewka_max_length = car._meta.get_field("gos_nom_in_putewka").max_length
        self.assertEqual(gos_nom_in_putewka_max_length, 4)

        state_number_unique = car._meta.get_field("state_number").unique
        self.assertEqual(state_number_unique, True)

        state_number_max_length = car._meta.get_field("state_number").max_length
        self.assertEqual(state_number_max_length, 16)

        name_unique = car._meta.get_field("name").unique
        self.assertEqual(name_unique, False)

        name_max_length = car._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 64)

        kod_driver_null = car._meta.get_field("kod_driver").null
        self.assertEqual(kod_driver_null, True)

        kod_driver_blank = car._meta.get_field("kod_driver").blank
        self.assertEqual(kod_driver_blank, True)

        date_decommissioned_null = car._meta.get_field("date_decommissioned").null
        self.assertEqual(date_decommissioned_null, True)

        date_decommissioned_blank = car._meta.get_field("date_decommissioned").blank
        self.assertEqual(date_decommissioned_blank, True)


class EmployeeModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )

    def test_fields(self):
        employee = Employee.objects.first()

        self.assertEqual(employee.__str__(), "Иванов И. И. (Слесарь)")
        self.assertEqual(employee.short_fio, "Иванов И. И.")
        self.assertEqual(employee.type_name, "Слесарь")

        number_in_kadry_unique = employee._meta.get_field("number_in_kadry").unique
        self.assertEqual(number_in_kadry_unique, True)

        first_name_max_length = employee._meta.get_field("first_name").max_length
        self.assertEqual(first_name_max_length, 24)

        last_name_max_length = employee._meta.get_field("last_name").max_length
        self.assertEqual(last_name_max_length, 24)

        patronymic_blank = employee._meta.get_field("patronymic").blank
        self.assertEqual(patronymic_blank, True)

        patronymic_max_length = employee._meta.get_field("patronymic").max_length
        self.assertEqual(patronymic_max_length, 24)

        type_choices = employee._meta.get_field("type").choices
        self.assertEqual(type_choices, EMPLOYEE_TYPE)

        position_max_length = employee._meta.get_field("position").max_length
        self.assertEqual(position_max_length, 32)

        date_dismissal_null = employee._meta.get_field("date_dismissal").null
        self.assertEqual(date_dismissal_null, True)

        date_dismissal_blank = employee._meta.get_field("date_dismissal").blank
        self.assertEqual(date_dismissal_blank, True)
