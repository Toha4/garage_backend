from django.db.models import PROTECT
from django.test import TestCase

from app.helpers.testing import get_test_user
from core.tests.factory import CarFactory

from .factory import CarTaskFactory


class CarTaskModelTestCase(TestCase):
    def setUp(self):
        user = get_test_user()
        car = CarFactory()
        self.car_task = CarTaskFactory(user=user, car=car)

    def test_fields(self):
        user_null = self.car_task._meta.get_field("user").null
        self.assertEqual(user_null, False)

        user_on_delete = self.car_task._meta.get_field("user").remote_field.on_delete
        self.assertEqual(user_on_delete, PROTECT)

        car_null = self.car_task._meta.get_field("car").null
        self.assertEqual(car_null, False)

        description_blank = self.car_task._meta.get_field("description").blank
        self.assertEqual(description_blank, True)

        materials_blank = self.car_task._meta.get_field("materials").blank
        self.assertEqual(materials_blank, True)

        is_completed_null = self.car_task._meta.get_field("is_completed").null
        self.assertEqual(is_completed_null, False)

        is_completed_default = self.car_task._meta.get_field("is_completed").default
        self.assertEqual(is_completed_default, False)

        date_completed_null = self.car_task._meta.get_field("date_completed").null
        self.assertEqual(date_completed_null, True)

        order_null = self.car_task._meta.get_field("order").null
        self.assertEqual(order_null, True)

        order_on_delete = self.car_task._meta.get_field("order").remote_field.on_delete
        self.assertEqual(order_on_delete, PROTECT)
