from factory.django import DjangoModelFactory

from ..models import Entrance
from ..models import Material
from ..models import MaterialCategory
from ..models import Turnover
from ..models import Unit
from ..models import Warehouse


class WarehouseFactory(DjangoModelFactory):
    name = "Главный склад"

    class Meta:
        model = Warehouse


class UnitFactory(DjangoModelFactory):
    name = "кг"
    is_precision_point = True

    class Meta:
        model = Unit


class MaterialCategoryFactory(DjangoModelFactory):
    name = "Масла"

    class Meta:
        model = MaterialCategory


class MaterialFactory(DjangoModelFactory):
    name = "Масло моторное IDEMITSU 5w30"
    unit = None
    category = None
    article_number = None
    compatbility = [
        "УАЗ 111",
    ]

    class Meta:
        model = Material


class EntranceFactory(DjangoModelFactory):
    user = None
    date = "2022-01-01"
    document_number = "A-111"
    responsible = None
    provider = "ОАО КАМАЗ"
    note = "Тестовое поступление"

    class Meta:
        model = Entrance


class TurnoverFactory(DjangoModelFactory):
    user = None
    type = None
    date = "2022-01-01"
    is_correction = False
    note = ""
    material = None
    warehouse = None
    price = 10.00
    quantity = 2.00
    sum = 20.00
    order = None
    entrance = None

    class Meta:
        model = Turnover
