from django.test import TestCase

from app.helpers.database import convert_to_localtime
from core.tests.factory import CarFactory
from core.tests.factory import EmployeeFactory

from ..api.serializers import OrderDetailSerializer
from ..api.serializers import OrderListSerializer
from ..api.serializers import PostSerializer
from ..api.serializers import ReasonSerializer
from ..api.serializers import WorkCategorySerializer
from ..api.serializers import WorkSerializer
from .factory import OrderFactory
from .factory import OrderWorkFactory
from .factory import OrderWorkMechanicFactory
from .factory import PostFactory
from .factory import ReasonFactory
from .factory import WorkCategoryFactory
from .factory import WorkFactory


class ReasonSerializerTestCase(TestCase):
    def test_ok(self):
        reason = ReasonFactory()
        data = ReasonSerializer(reason).data
        expected_data = {
            "pk": reason.pk,
            "name": "ТО",
            "type": 1,
        }
        self.assertEqual(expected_data, data)


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        post = PostFactory()
        data = PostSerializer(post).data
        expected_data = {
            "pk": post.pk,
            "name": "Бокс 1",
        }
        self.assertEqual(expected_data, data)


class OrderSerializerTestCase(TestCase):
    def test_list(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(reason=reason, post=post, car=car, driver=driver, responsible=responsible)

        data = OrderListSerializer(order).data
        expected_data = {
            "pk": order.pk,
            "number": 1,
            "date_begin": "2022-01-01 12:00",
            "status_name": "Заяка",
            "car_name": "УАЗ 111",
            "car_state_number": "А 777 АА",
            "post_name": "Бокс 1",
            "reason_name": "ТО",
            "note": "Тестовый заказ-наряд",
        }
        self.assertEqual(expected_data, data)

    def test_detail(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(reason=reason, post=post, car=car, driver=driver, responsible=responsible)
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        order_work = OrderWorkFactory(order=order, work=work)
        mechanic = EmployeeFactory(number_in_kadry=3, type=2, position="Слесарь")
        order_work_mechanic = OrderWorkMechanicFactory(order_work=order_work, mechanic=mechanic)

        data = OrderDetailSerializer(order).data
        expected_data = {
            "pk": order.pk,
            "created": convert_to_localtime(order.created).strftime("%d.%m.%Y %H:%M"),
            "updated": convert_to_localtime(order.updated).strftime("%d.%m.%Y %H:%M"),
            "number": 1,
            "status": 1,
            "reason": reason.pk,
            "date_begin": "2022-01-01 12:00",
            "date_end": None,
            "post": post.pk,
            "car": car.pk,
            "driver": driver.pk,
            "responsible": responsible.pk,
            "odometer": 123000,
            "note": "Тестовый заказ-наряд",
            "order_works": [
                {
                    "pk": order_work.pk,
                    "work": order_work.work.pk,
                    "quantity": 1,
                    "time_minutes": 120,
                    "note": "Тестовая работа",
                    "mechanics": [
                        {"pk": order_work_mechanic.pk, "mechanic": order_work_mechanic.mechanic.pk, "time_minutes": 60}
                    ],
                }
            ],
        }
        self.assertEqual(expected_data, data)


class WorkCategorySerializerTestCase(TestCase):
    def test_ok(self):
        work_category = WorkCategoryFactory()
        data = WorkCategorySerializer(work_category).data
        expected_data = {
            "pk": work_category.pk,
            "name": "Электрика",
        }
        self.assertEqual(expected_data, data)


class WorkSerializerTestCase(TestCase):
    def test_ok(self):
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        data = WorkSerializer(work).data
        expected_data = {
            "pk": work.pk,
            "name": "Замена аккумулятора",
            "category": work_category.pk,
        }
        self.assertEqual(expected_data, data)
