import json

from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase
from app.helpers.testing import DecimalEncoder
from app.helpers.testing import get_test_user
from core.tests.factory import EmployeeFactory
from warehouse.constants import COMING
from warehouse.helpers.get_queryset_materials_remains import get_queryset_materials_remains

from ...api.serializers import MaterialAvailabilitySerializer
from ...api.serializers import MaterialListSerializer
from ...api.serializers import MaterialRemainsCategorySerializer
from ...api.serializers import MaterialRemainsSerializer
from ...api.serializers import MaterialSerializer
from ...models import Material
from ..factory import EntranceFactory
from ..factory import MaterialCategoryFactory
from ..factory import MaterialFactory
from ..factory import TurnoverFactory
from ..factory import UnitFactory
from ..factory import WarehouseFactory


class MaterialApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        unit1 = UnitFactory()
        category1 = MaterialCategoryFactory()
        material1 = MaterialFactory(unit=unit1, category=category1)

        unit2 = UnitFactory(name="шт", is_precision_point=False)
        category2 = MaterialCategoryFactory(name="Фильтра")
        material2 = MaterialFactory(name="Фильтр воздушный NF300", unit=unit2, category=category2)

        url = reverse("material-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Material.objects.filter(pk__in=[material1.pk, material2.pk])
        serializer_data = MaterialListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

        # category_filter
        response_category_filter = self.client.get(url, {"category": category2.pk})
        self.assertEqual(status.HTTP_200_OK, response_category_filter.status_code)
        queryset = Material.objects.filter(category=category2.pk)
        serializer_data = MaterialListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response_category_filter.data)

        # general_search
        response_general_search = self.client.get(url, {"general_search": "масло"})
        self.assertEqual(status.HTTP_200_OK, response_general_search.status_code)
        serializer_data = MaterialListSerializer([material1], many=True).data
        self.assertEqual(serializer_data, response_general_search.data)

    def test_get_list_material_remains(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("material-remains-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = get_queryset_materials_remains(None, None, None, None, None, False)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": json.loads(json.dumps(MaterialRemainsSerializer(queryset, many=True).data, cls=DecimalEncoder)),
        }
        self.assertEqual(serializer_data, response.data)

    def test_get_list_material_remains_category(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("material-remains-category-list")
        response = self.client.get(url, {"category": category.pk})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = get_queryset_materials_remains(None, None, None, "true", None, True)
        serializer_data = json.loads(
            json.dumps(MaterialRemainsCategorySerializer(queryset, many=True).data, cls=DecimalEncoder)
        )
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        payload = {
            "name": "Масло моторное IDEMITSU 5w30",
            "unit": unit.pk,
            "category": category.pk,
            "compatbility": [
                "УАЗ 111",
            ],
        }

        url = reverse("material-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Material.objects.get(name=payload["name"]))

    def test_get(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        url = reverse("material-detail", kwargs={"pk": material.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = MaterialSerializer(material).data
        self.assertEqual(serializer_data, response.data)

    def test_get_availability_mode(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        user = get_test_user()
        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("material-detail", kwargs={"pk": material.pk})
        response = self.client.get(url, {"availability_mode": "true"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = MaterialAvailabilitySerializer(material).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        unit1 = UnitFactory()
        category1 = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit1, category=category1)

        unit2 = UnitFactory(name="шт", is_precision_point=False)
        category2 = MaterialCategoryFactory(name="Фильтра")
        payload = {
            "name": "Фильтр воздушный NF300",
            "unit": unit2.pk,
            "category": category2.pk,
            "compatbility": [
                "КИА БОНГО",
            ],
        }

        url = reverse("material-detail", kwargs={"pk": material.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        material_result = Material.objects.get(pk=material.pk)
        self.assertEqual(material_result.name, payload["name"])

    def test_delete(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)

        url = reverse("material-detail", kwargs={"pk": material.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Material.DoesNotExist):
            Material.objects.get(pk=material.pk)
