import json

from django.test import TestCase

from app.helpers.database import convert_to_localtime
from app.helpers.testing import DecimalEncoder
from app.helpers.testing import get_test_user
from core.tests.factory import CarFactory
from core.tests.factory import EmployeeFactory
from warehouse.constants import COMING
from warehouse.constants import EXPENSE
from warehouse.tests.factory import EntranceFactory
from warehouse.tests.factory import MaterialCategoryFactory
from warehouse.tests.factory import MaterialFactory
from warehouse.tests.factory import TurnoverFactory
from warehouse.tests.factory import UnitFactory
from warehouse.tests.factory import WarehouseFactory

from ..api.serializers import OrderDetailSerializer
from ..api.serializers import OrderListSerializer
from ..api.serializers import PostListSerializer
from ..api.serializers import PostSerializer
from ..api.serializers import ReasonListSerializer
from ..api.serializers import ReasonSerializer
from ..api.serializers import WorkCategoryListSerializer
from ..api.serializers import WorkCategorySerializer
from ..api.serializers import WorkListSerializer
from ..api.serializers import WorkSerializer
from ..constants import REQUEST
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


class ReasonListSerializerTestCase(TestCase):
    def test_ok(self):
        reason = ReasonFactory()
        data = ReasonListSerializer(reason).data
        expected_data = {
            "pk": reason.pk,
            "name": "ТО",
            "type": 1,
            "delete_forbidden": False,
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


class PostListSerializerTestCase(TestCase):
    def test_ok(self):
        post = PostFactory()
        data = PostListSerializer(post).data
        expected_data = {
            "pk": post.pk,
            "name": "Бокс 1",
            "delete_forbidden": False,
        }
        self.assertEqual(expected_data, data)


class OrderSerializerTestCase(TestCase):
    def test_list(self):
        user = get_test_user()

        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(user=user, post=post, car=car, driver=driver, responsible=responsible)
        order.reasons.add(reason)

        data = OrderListSerializer(order).data
        expected_data = {
            "pk": order.pk,
            "number": 1,
            "date_begin": "2022-01-01 12:00",
            "status": REQUEST,
            "status_name": "Заяка",
            "car_name": "УАЗ 111",
            "car_state_number": "А 777 АА",
            "post_name": "Бокс 1",
            "reason_name": "ТО",
            "note": "Тестовый заказ-наряд",
        }
        self.assertEqual(expected_data, data)

    def test_detail(self):
        user = get_test_user()

        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(user=user, post=post, car=car, driver=driver, responsible=responsible)
        order.reasons.add(reason)

        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        order_work = OrderWorkFactory(order=order, work=work)
        mechanic = EmployeeFactory(number_in_kadry=3, type=2, position="Слесарь")
        order_work_mechanic = OrderWorkMechanicFactory(order_work=order_work, mechanic=mechanic)

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover_entrance = TurnoverFactory(
            user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance
        )
        turnover_order = TurnoverFactory(user=user, type=EXPENSE, material=material, warehouse=warehouse, order=order)

        data = OrderDetailSerializer(order).data
        data = json.loads(json.dumps(OrderDetailSerializer(order).data, cls=DecimalEncoder))
        expected_data = {
            "pk": order.pk,
            "created": convert_to_localtime(order.created).strftime("%d.%m.%Y %H:%M"),
            "updated": convert_to_localtime(order.updated).strftime("%d.%m.%Y %H:%M"),
            "number": 1,
            "status": 1,
            "reasons": [reason.pk],
            "date_begin": "2022-01-01 12:00",
            "date_end": None,
            "post": post.pk,
            "car": car.pk,
            "car_name": car.name,
            "car_task_count": 0,
            "driver": driver.pk,
            "responsible": responsible.pk,
            "odometer": 123000,
            "note": "Тестовый заказ-наряд",
            "order_works": [
                {
                    "pk": order_work.pk,
                    "work": order_work.work.pk,
                    "work_name": order_work.work.name,
                    "work_category": order_work.work.category.pk,
                    "quantity": 1,
                    "time_minutes": 120,
                    "note": "Тестовая работа",
                    "mechanics": [
                        {
                            "pk": order_work_mechanic.pk,
                            "mechanic": order_work_mechanic.mechanic.pk,
                            "mechanic_short_fio": order_work_mechanic.mechanic.short_fio,
                            "time_minutes": 60,
                        }
                    ],
                }
            ],
            "turnovers_from_order": [
                {
                    "pk": turnover_order.pk,
                    "type": turnover_order.type,
                    "date": "01.01.2022",
                    "is_correction": False,
                    "note": "",
                    "material": turnover_order.material.pk,
                    "material_name": "Масло моторное IDEMITSU 5w30",
                    "material_unit_name": "кг",
                    "material_unit_is_precision_point": True,
                    "warehouse": turnover_order.warehouse.pk,
                    "warehouse_name": "Главный склад",
                    "price": 10.0,
                    "quantity": 2.0,
                    "sum": 20.0,
                    "order": order.pk,
                    "entrance": None,
                },
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


class WorkCategoryListSerializerTestCase(TestCase):
    def test_ok(self):
        work_category = WorkCategoryFactory()
        WorkFactory(category=work_category)
        data = WorkCategoryListSerializer(work_category).data
        expected_data = {
            "pk": work_category.pk,
            "name": "Электрика",
            "work_count": 1,
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


class WorkListSerializerTestCase(TestCase):
    def test_ok(self):
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        data = WorkListSerializer(work).data
        expected_data = {
            "pk": work.pk,
            "name": "Замена аккумулятора",
            "category": work_category.pk,
            "delete_forbidden": False,
        }
        self.assertEqual(expected_data, data)
