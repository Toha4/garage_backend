import json

from django.test import TestCase

from app.helpers.testing import DecimalEncoder
from app.helpers.testing import get_test_user
from core.tests.factory import EmployeeFactory

from ..api.serializers import EntranceListSerializer
from ..api.serializers import EntranceSerializer
from ..api.serializers import MaterialAvailabilitySerializer
from ..api.serializers import MaterialCategoryListSerializer
from ..api.serializers import MaterialCategorySerializer
from ..api.serializers import MaterialListSerializer
from ..api.serializers import MaterialRemainsCategorySerializer
from ..api.serializers import MaterialRemainsSerializer
from ..api.serializers import MaterialSerializer
from ..api.serializers import TurnoverMaterialReadSerializer
from ..api.serializers import TurnoverSerializer
from ..api.serializers import UnitSerializer
from ..api.serializers import WarehouseListSerializer
from ..api.serializers import WarehouseSerializer
from ..constants import COMING
from ..helpers.get_queryset_materials_remains import get_queryset_materials_remains
from .factory import EntranceFactory
from .factory import MaterialCategoryFactory
from .factory import MaterialFactory
from .factory import TurnoverFactory
from .factory import UnitFactory
from .factory import WarehouseFactory


class WarehouseSerializerTestCase(TestCase):
    def test_ok(self):
        warehouse = WarehouseFactory()
        data = WarehouseSerializer(warehouse).data
        expected_data = {
            "pk": warehouse.pk,
            "name": "Главный склад",
        }
        self.assertEqual(expected_data, data)


class WarehouseListSerializerTestCase(TestCase):
    def test_ok(self):
        warehouse = WarehouseFactory()
        data = WarehouseListSerializer(warehouse).data
        expected_data = {
            "pk": warehouse.pk,
            "name": "Главный склад",
            "delete_forbidden": False,
        }
        self.assertEqual(expected_data, data)


class UnitSerializerTestCase(TestCase):
    def test_ok(self):
        unit = UnitFactory()
        data = UnitSerializer(unit).data
        expected_data = {
            "pk": unit.pk,
            "name": "кг",
            "is_precision_point": True,
        }
        self.assertEqual(expected_data, data)


class MaterialCategorySerializerTestCase(TestCase):
    def test_ok(self):
        material_category = MaterialCategoryFactory()
        data = MaterialCategorySerializer(material_category).data
        expected_data = {
            "pk": material_category.pk,
            "name": "Масла",
        }
        self.assertEqual(expected_data, data)


class MaterialCategoryListSerializerTestCase(TestCase):
    def test_ok(self):
        material_category = MaterialCategoryFactory()
        data = MaterialCategoryListSerializer(material_category).data
        expected_data = {
            "pk": material_category.pk,
            "name": "Масла",
            "material_count": 0,
        }
        self.assertEqual(expected_data, data)


class MaterialSerializerTestCase(TestCase):
    def test_ok(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category, article_number="A123456")
        data = MaterialSerializer(material).data
        expected_data = {
            "pk": material.pk,
            "name": "Масло моторное IDEMITSU 5w30",
            "unit": unit.pk,
            "category": category.pk,
            "article_number": "A123456",
            "compatbility": [
                "УАЗ 111",
            ],
        }
        self.assertEqual(expected_data, data)


class MaterialListSerializerTestCase(TestCase):
    def test_ok(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        data = MaterialListSerializer(material).data
        expected_data = {
            "pk": material.pk,
            "name": "Масло моторное IDEMITSU 5w30",
            "unit": unit.pk,
            "category": category.pk,
            "article_number": None,
            "compatbility": [
                "УАЗ 111",
            ],
            "delete_forbidden": False,
            "unit_name": "кг",
            "unit_is_precision_point": True,
        }
        self.assertEqual(expected_data, data)


class MaterialAvailabilitySerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        data = json.loads(json.dumps(MaterialAvailabilitySerializer(material).data, cls=DecimalEncoder))
        expected_data = {
            "id": material.id,
            "name": "Масло моторное IDEMITSU 5w30",
            "warehouses_availability": [
                {
                    "warehouse": turnover.warehouse.id,
                    "warehouse_name": "Главный склад",
                    "quantity": 2.0,
                    "prices": {"average_price": 10.0, "last_price": 10.0},
                }
            ],
            "prices": {"average_price": 10.0, "last_price": 10.0},
            "quantity": 2.0,
            "unit_name": "кг",
            "unit_is_precision_point": True,
        }
        self.assertEqual(expected_data, data)


class TurnoverSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        data = json.loads(json.dumps(TurnoverSerializer(turnover).data, cls=DecimalEncoder))
        expected_data = {
            "pk": turnover.id,
            "type": 1,
            "date": "2022-01-01",
            "is_correction": False,
            "note": "",
            "material": turnover.material.id,
            "material_name": "Масло моторное IDEMITSU 5w30",
            "material_unit_name": "кг",
            "material_unit_is_precision_point": True,
            "warehouse": turnover.warehouse.id,
            "warehouse_name": "Главный склад",
            "price": 10.0,
            "quantity": 2.0,
            "sum": 20.0,
            "order": None,
            "entrance": entrance.id,
        }
        self.assertEqual(expected_data, data)


class TurnoverNestedWriteSerializerTestCase(TestCase):
    pass


class TurnoverMaterialReadSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        data = json.loads(json.dumps(TurnoverMaterialReadSerializer(turnover).data, cls=DecimalEncoder))
        expected_data = {
            "id": turnover.id,
            "type": 1,
            "date": "2022-01-01",
            "is_correction": False,
            "user_name": "Last F I",
            "turnover_name": "Приход от ОАО КАМАЗ (№ документа A-111)",
            "warehouse_name": "Главный склад",
            "quantity": 2.0,
            "quantity_with_unit": "2.0 кг",
            "price": 10.0,
            "sum": 20.0,
            "order": None,
            "entrance": entrance.id,
        }
        self.assertEqual(expected_data, data)


class TurnoverMovingMaterialSerializerTestCase(TestCase):
    pass


class EntranceListSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)

        data = EntranceListSerializer(entrance).data
        expected_data = {
            "pk": entrance.id,
            "date": "2022-01-01",
            "document_number": "A-111",
            "provider": "ОАО КАМАЗ",
            "note": "Тестовое поступление",
        }
        self.assertEqual(expected_data, data)


class EntranceSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        data = json.loads(json.dumps(EntranceSerializer(entrance).data, cls=DecimalEncoder))
        expected_data = {
            "pk": entrance.id,
            "date": "2022-01-01",
            "document_number": "A-111",
            "responsible": entrance.responsible.id,
            "provider": "ОАО КАМАЗ",
            "note": "Тестовое поступление",
            "turnovers_from_entrance": [
                {
                    "pk": turnover.id,
                    "type": 1,
                    "date": "01.01.2022",
                    "is_correction": False,
                    "note": "",
                    "material": turnover.material.id,
                    "material_name": "Масло моторное IDEMITSU 5w30",
                    "material_unit_name": "кг",
                    "material_unit_is_precision_point": True,
                    "warehouse": turnover.warehouse.id,
                    "warehouse_name": "Главный склад",
                    "price": 10.0,
                    "quantity": 2.0,
                    "sum": 20.0,
                    "order": None,
                    "entrance": turnover.entrance.id,
                }
            ],
        }
        self.assertEqual(expected_data, data)


class MaterialRemainsSerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        queryset = get_queryset_materials_remains(None, None, None, None, None, False)
        data = json.loads(json.dumps(MaterialRemainsSerializer(queryset, many=True).data, cls=DecimalEncoder))

        expected_data = [
            {
                "id": material.id,
                "name": "Масло моторное IDEMITSU 5w30",
                "category": material.category.id,
                "category_name": "Масла",
                "unit_name": "кг",
                "unit_is_precision_point": True,
                "compatbility": ["УАЗ 111"],
                "warehouses_availability": [
                    {
                        "warehouse": turnover.warehouse.id,
                        "warehouse_name": "Главный склад",
                        "quantity": 2.0,
                        "prices": {"average_price": 10.0, "last_price": 10.0},
                    }
                ],
                "quantity": 2.0,
                "price": 10.0,
                "sum": 20.0,
            }
        ]
        self.assertEqual(expected_data, data)


class MaterialRemainsCategorySerializerTestCase(TestCase):
    def test_ok(self):
        user = get_test_user()
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        queryset = get_queryset_materials_remains(None, None, None, "true", None, True)
        data = json.loads(json.dumps(MaterialRemainsCategorySerializer(queryset, many=True).data, cls=DecimalEncoder))
        expected_data = [
            {
                "id": material.id,
                "name": "Масло моторное IDEMITSU 5w30",
                "category": material.category.id,
                "unit_name": "кг",
                "unit_is_precision_point": True,
                "warehouse": warehouse.id,
                "warehouse_name": "Главный склад",
                "compatbility": ["УАЗ 111"],
                "quantity": 2.0,
                "price": 10.0,
                "sum": 20.0,
            }
        ]
        self.assertEqual(expected_data, data)
