from factory.django import DjangoModelFactory

from ..constants import REQUEST
from ..models import Order
from ..models import OrderWork
from ..models import OrderWorkMechanic
from ..models import Post
from ..models import Reason
from ..models import Work
from ..models import WorkCategory


class ReasonFactory(DjangoModelFactory):
    name = "ТО"
    type = 1

    class Meta:
        model = Reason


class PostFactory(DjangoModelFactory):
    name = "Бокс 1"

    class Meta:
        model = Post


class OrderFactory(DjangoModelFactory):
    user = None
    number = None
    status = REQUEST
    date_begin = "2022-01-01 12:00"
    date_end = None
    post = None
    car = None
    driver = None
    responsible = None
    odometer = 123000
    note = "Тестовый заказ-наряд"

    class Meta:
        model = Order


class WorkCategoryFactory(DjangoModelFactory):
    name = "Электрика"

    class Meta:
        model = WorkCategory


class WorkFactory(DjangoModelFactory):
    name = "Замена аккумулятора"
    category = None

    class Meta:
        model = Work


class OrderWorkFactory(DjangoModelFactory):
    order = None
    work = None
    quantity = 1
    time_minutes = 120
    note = "Тестовая работа"

    class Meta:
        model = OrderWork


class OrderWorkMechanicFactory(DjangoModelFactory):
    order_work = None
    mechanic = None
    time_minutes = 60

    class Meta:
        model = OrderWorkMechanic
