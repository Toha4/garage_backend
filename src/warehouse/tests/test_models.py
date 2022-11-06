from django.db.models import PROTECT
from django.test import TestCase

from app.helpers.testing import get_test_user
from core.tests.factory import EmployeeFactory

from ..constants import COMING
from ..constants import TURNOVER_TYPE
from .factory import EntranceFactory
from .factory import MaterialCategoryFactory
from .factory import MaterialFactory
from .factory import TurnoverFactory
from .factory import UnitFactory
from .factory import WarehouseFactory


class WarehouseModelTestCase(TestCase):
    def setUp(self):
        self.warehouse = WarehouseFactory()

    def test_fields(self):
        name_unique = self.warehouse._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.warehouse._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)


class UnitModelTestCase(TestCase):
    def setUp(self):
        self.unit = UnitFactory()

    def test_fields(self):
        name_unique = self.unit._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.unit._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 16)

        is_precision_point_default = self.unit._meta.get_field("is_precision_point").default
        self.assertEqual(is_precision_point_default, False)


class MaterialCategoryModelTestCase(TestCase):
    def setUp(self):
        self.material_category = MaterialCategoryFactory()

    def test_fields(self):
        name_unique = self.material_category._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.material_category._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 32)


class MaterialModelTestCase(TestCase):
    def setUp(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        self.material = MaterialFactory(unit=unit, category=category)

    def test_fields(self):
        name_unique = self.material._meta.get_field("name").unique
        self.assertEqual(name_unique, True)

        name_max_length = self.material._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 128)

        category_on_delete = self.material._meta.get_field("category").remote_field.on_delete
        self.assertEqual(category_on_delete, PROTECT)

        article_number_max_length = self.material._meta.get_field("article_number").max_length
        self.assertEqual(article_number_max_length, 32)

        article_number_blank = self.material._meta.get_field("article_number").blank
        self.assertEqual(article_number_blank, True)

        compatbility_blank = self.material._meta.get_field("compatbility").blank
        self.assertEqual(compatbility_blank, True)


class EntranceModelTestCase(TestCase):
    def setUp(self):
        user = get_test_user()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        self.entrance = EntranceFactory(user=user, responsible=responsible)

    def test_fields(self):
        user_null = self.entrance._meta.get_field("user").null
        self.assertEqual(user_null, False)

        date_null = self.entrance._meta.get_field("date").null
        self.assertEqual(date_null, False)

        document_number_max_length = self.entrance._meta.get_field("document_number").max_length
        self.assertEqual(document_number_max_length, 64)

        document_number_blank = self.entrance._meta.get_field("document_number").blank
        self.assertEqual(document_number_blank, True)

        responsible_on_delete = self.entrance._meta.get_field("responsible").remote_field.on_delete
        self.assertEqual(responsible_on_delete, PROTECT)

        responsible_null = self.entrance._meta.get_field("responsible").null
        self.assertEqual(responsible_null, False)

        provider_max_length = self.entrance._meta.get_field("provider").max_length
        self.assertEqual(provider_max_length, 128)

        provider_blank = self.entrance._meta.get_field("provider").blank
        self.assertEqual(provider_blank, True)

        note_blank = self.entrance._meta.get_field("note").blank
        self.assertEqual(note_blank, True)


class TurnoverModelTestCase(TestCase):
    def setUp(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)

        self.turnover = TurnoverFactory(
            user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance
        )

    def test_fields(self):
        type_choices = self.turnover._meta.get_field("type").choices
        self.assertEqual(type_choices, TURNOVER_TYPE)

        date_null = self.turnover._meta.get_field("date").null
        self.assertEqual(date_null, False)

        is_correction_default = self.turnover._meta.get_field("is_correction").default
        self.assertEqual(is_correction_default, False)

        note_blank = self.turnover._meta.get_field("note").blank
        self.assertEqual(note_blank, True)

        user_null = self.turnover._meta.get_field("user").null
        self.assertEqual(user_null, False)

        material_null = self.turnover._meta.get_field("material").null
        self.assertEqual(material_null, False)

        material_on_delete = self.turnover._meta.get_field("material").remote_field.on_delete
        self.assertEqual(material_on_delete, PROTECT)

        material_null = self.turnover._meta.get_field("material").null
        self.assertEqual(material_null, False)

        material_on_delete = self.turnover._meta.get_field("material").remote_field.on_delete
        self.assertEqual(material_on_delete, PROTECT)

        price_max_digits = self.turnover._meta.get_field("price").max_digits
        self.assertEqual(price_max_digits, 12)

        price_decimal_places = self.turnover._meta.get_field("price").decimal_places
        self.assertEqual(price_decimal_places, 2)

        quantity_max_digits = self.turnover._meta.get_field("quantity").max_digits
        self.assertEqual(quantity_max_digits, 9)

        quantity_decimal_places = self.turnover._meta.get_field("quantity").decimal_places
        self.assertEqual(quantity_decimal_places, 2)

        sum_max_digits = self.turnover._meta.get_field("sum").max_digits
        self.assertEqual(sum_max_digits, 12)

        sum_decimal_places = self.turnover._meta.get_field("sum").decimal_places
        self.assertEqual(sum_decimal_places, 2)

        order_null = self.turnover._meta.get_field("order").null
        self.assertEqual(order_null, True)

        order_blank = self.turnover._meta.get_field("order").blank
        self.assertEqual(order_blank, True)

        entrance_null = self.turnover._meta.get_field("entrance").null
        self.assertEqual(entrance_null, True)

        entrance_blank = self.turnover._meta.get_field("entrance").blank
        self.assertEqual(entrance_blank, True)
