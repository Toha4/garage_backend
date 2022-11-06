from django.test import TestCase

from ..api.serializers import CarDetailSerializer
from ..api.serializers import CarShortSerializer
from ..api.serializers import CarTagSerializer
from ..api.serializers import EmployeeDetailSerializer
from ..api.serializers import EmployeeShortSerializer
from .factory import CarFactory
from .factory import EmployeeFactory


class CarSerializerTestCase(TestCase):
    def test_short(self):
        car = CarFactory()
        data = CarShortSerializer(car).data
        expected_data = {"pk": car.pk, "state_number": "А 777 АА", "name": "УАЗ 111"}
        self.assertEqual(expected_data, data)

    def test_detail(self):
        car = CarFactory()
        data = CarDetailSerializer(car).data
        expected_data = {
            "pk": car.pk,
            "kod_mar_in_putewka": 1,
            "gos_nom_in_putewka": "777",
            "state_number": "А 777 АА",
            "name": "УАЗ 111",
            "kod_driver": 11,
            "driver_pk": None,
            "date_decommissioned": None,
        }
        self.assertEqual(expected_data, data)


class CarTagSerializerTestCase(TestCase):
    def test_ok(self):
        car1 = CarFactory()
        car2 = CarFactory(kod_mar_in_putewka=2, gos_nom_in_putewka="666", state_number="А 666 АА", name="КАМАЗ 5000")
        data = CarTagSerializer([car1, car2], many=True).data
        expected_data = [{"name": "УАЗ 111"}, {"name": "КАМАЗ 5000"}]
        self.assertEqual(expected_data, data)


class EmployeeSerializerTestCase(TestCase):
    def test_short(self):
        employee = EmployeeFactory()
        data = EmployeeShortSerializer(employee).data
        expected_data = {"pk": employee.pk, "short_fio": "Иванов И. И.", "type": 2}
        self.assertEqual(expected_data, data)

    def test_detail(self):
        employee = EmployeeFactory()
        data = EmployeeDetailSerializer(employee).data
        expected_data = {
            "pk": employee.pk,
            "number_in_kadry": 1,
            "short_fio": "Иванов И. И.",
            "first_name": "Иван",
            "last_name": "Иванов",
            "patronymic": "Иванович",
            "type": 2,
            "position": "Слесарь 1 раз.",
            "date_dismissal": None,
        }
        self.assertEqual(expected_data, data)
