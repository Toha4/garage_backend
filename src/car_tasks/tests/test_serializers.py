from django.test import TestCase

from app.helpers.database import convert_to_localtime
from app.helpers.testing import get_test_user
from core.tests.factory import CarFactory

from ..api.serializers import CarTaskListSerializer
from ..api.serializers import CarTaskSerializer
from .factory import CarTaskFactory


class CarTaskSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        data = CarTaskSerializer(car_task).data
        expected_data = {
            "pk": car_task.pk,
            "created": convert_to_localtime(car_task.created).strftime("%d.%m.%Y"),
            "car": car.pk,
            "description": "Заменить воздушный фильтр",
            "materials": "Фильтр воздушеый арт. 0K6B023603",
            "is_completed": False,
            "date_completed": None,
            "order": None,
        }
        self.assertEqual(expected_data, data)


class CarTaskListSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        data = CarTaskListSerializer(car_task).data
        expected_data = {
            "pk": car_task.pk,
            "created": convert_to_localtime(car_task.created).strftime("%d.%m.%Y"),
            "car": car.pk,
            "description": "Заменить воздушный фильтр",
            "materials": "Фильтр воздушеый арт. 0K6B023603",
            "is_completed": False,
            "date_completed": None,
            "order": None,
            "car_name": "А 777 АА - УАЗ 111",
            "order_number": None,
        }
        self.assertEqual(expected_data, data)
