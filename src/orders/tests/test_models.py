from django.db.models import CASCADE
from django.db.models import PROTECT
from django.test import TestCase

from core.tests.factory import CarFactory
from core.tests.factory import EmployeeFactory

from ..constants import ORDER_STATUS
from ..constants import REASON_TYPE
from ..models import Order
from .factory import OrderFactory
from .factory import OrderWorkFactory
from .factory import OrderWorkMechanicFactory
from .factory import PostFactory
from .factory import ReasonFactory
from .factory import WorkCategoryFactory
from .factory import WorkFactory


class ReasonModelTestCase(TestCase):
    def setUp(self):
        self.reason = ReasonFactory()

    def test_fields(self):
        name_unique = self.reason._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.reason._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)

        type_choices = self.reason._meta.get_field("type").choices
        self.assertEqual(type_choices, REASON_TYPE)


class PostModelTestCase(TestCase):
    def setUp(self):
        self.post = PostFactory()

    def test_fields(self):
        name_unique = self.post._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.post._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 16)


class OrderModelTestCase(TestCase):
    def setUp(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        self.order = OrderFactory(reason=reason, post=post, car=car, driver=driver, responsible=responsible)

    def test_fields(self):
        order = Order.objects.first()

        self.assertEqual(order.__str__(), f"{order.number} - 01.01.2022 - {order.car}")

        number_unique = order._meta.get_field("number").unique
        self.assertEqual(number_unique, True)

        status_choices = order._meta.get_field("status").choices
        self.assertEqual(status_choices, ORDER_STATUS)

        reason_on_delete = order._meta.get_field("reason").remote_field.on_delete
        self.assertEqual(reason_on_delete, PROTECT)

        date_begin_null = order._meta.get_field("date_begin").null
        self.assertEqual(date_begin_null, False)

        date_end_null = order._meta.get_field("date_end").null
        self.assertEqual(date_end_null, True)

        date_end_blank = order._meta.get_field("date_end").blank
        self.assertEqual(date_end_blank, True)

        post_on_delete = order._meta.get_field("post").remote_field.on_delete
        self.assertEqual(post_on_delete, PROTECT)

        post_null = order._meta.get_field("post").null
        self.assertEqual(post_null, True)

        post_blank = order._meta.get_field("post").blank
        self.assertEqual(post_blank, True)

        car_on_delete = order._meta.get_field("car").remote_field.on_delete
        self.assertEqual(car_on_delete, PROTECT)

        driver_on_delete = order._meta.get_field("driver").remote_field.on_delete
        self.assertEqual(driver_on_delete, PROTECT)

        driver_null = order._meta.get_field("driver").null
        self.assertEqual(driver_null, True)

        driver_blank = order._meta.get_field("driver").blank
        self.assertEqual(driver_blank, True)

        responsible_on_delete = order._meta.get_field("responsible").remote_field.on_delete
        self.assertEqual(responsible_on_delete, PROTECT)

        responsible_null = order._meta.get_field("responsible").null
        self.assertEqual(responsible_null, True)

        responsible_blank = order._meta.get_field("responsible").blank
        self.assertEqual(responsible_blank, True)

        odometer_null = order._meta.get_field("odometer").null
        self.assertEqual(odometer_null, True)

        odometer_blank = order._meta.get_field("odometer").blank
        self.assertEqual(odometer_blank, True)

        note_blank = order._meta.get_field("note").blank
        self.assertEqual(note_blank, True)


class WorkCategoryModelTestCase(TestCase):
    def setUp(self):
        self.work_category = WorkCategoryFactory()

    def test_fields(self):
        name_unique = self.work_category._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.work_category._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)


class WorkModelTestCase(TestCase):
    def setUp(self):
        work_category = WorkCategoryFactory()
        self.work = WorkFactory(category=work_category)

    def test_fields(self):
        name_unique = self.work._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.work._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)

        category_on_delete = self.work._meta.get_field("category").remote_field.on_delete
        self.assertEqual(category_on_delete, PROTECT)


class OrderWorkModelTestCase(TestCase):
    def setUp(self):
        reason = ReasonFactory()
        car = CarFactory()
        order = OrderFactory(reason=reason, car=car)
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        self.order_work = OrderWorkFactory(order=order, work=work)

    def test_fields(self):
        order_on_delete = self.order_work._meta.get_field("order").remote_field.on_delete
        self.assertEqual(order_on_delete, CASCADE)

        work_on_delete = self.order_work._meta.get_field("work").remote_field.on_delete
        self.assertEqual(work_on_delete, PROTECT)

        time_minutes_null = self.order_work._meta.get_field("time_minutes").null
        self.assertEqual(time_minutes_null, True)

        time_minutes_blank = self.order_work._meta.get_field("time_minutes").blank
        self.assertEqual(time_minutes_blank, True)


class OrderWorkMechanicModelTestCase(TestCase):
    def setUp(self):
        reason = ReasonFactory()
        car = CarFactory()
        order = OrderFactory(reason=reason, car=car)
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        order_work = OrderWorkFactory(order=order, work=work)
        mechanic = EmployeeFactory(type=2, position="Слесарь")
        self.order_work_mechanic = OrderWorkMechanicFactory(order_work=order_work, mechanic=mechanic)

    def test_fields(self):
        order_work_on_delete = self.order_work_mechanic._meta.get_field("order_work").remote_field.on_delete
        self.assertEqual(order_work_on_delete, CASCADE)

        mechanic_on_delete = self.order_work_mechanic._meta.get_field("mechanic").remote_field.on_delete
        self.assertEqual(mechanic_on_delete, PROTECT)

        time_minutes_null = self.order_work_mechanic._meta.get_field("time_minutes").null
        self.assertEqual(time_minutes_null, True)

        time_minutes_blank = self.order_work_mechanic._meta.get_field("time_minutes").blank
        self.assertEqual(time_minutes_blank, True)
