import json

from django.db.models.deletion import ProtectedError
from django.urls import reverse

from rest_framework import status

from app.helpers.database import get_period_filter_lookup
from app.helpers.testing import AuthorizationAPITestCase
from app.helpers.testing import get_test_user
from core.tests.factory import EmployeeFactory

from ...api.serializers import EntranceListSerializer
from ...api.serializers import EntranceSerializer
from ...constants import COMING
from ...models import Entrance
from ...tests.factory import EntranceFactory
from ...tests.factory import MaterialCategoryFactory
from ...tests.factory import MaterialFactory
from ...tests.factory import TurnoverFactory
from ...tests.factory import UnitFactory
from ...tests.factory import WarehouseFactory


class EntranceApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance1 = EntranceFactory(user=user, responsible=responsible)
        turnover1 = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance1)

        entrance2 = EntranceFactory(user=user, date="2022-01-17", document_number="A-222", responsible=responsible)
        turnover2 = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance2)

        url = reverse("entrance-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Entrance.objects.filter(pk__in=[entrance1.pk, entrance2.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": EntranceListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # date_filter
        date_begin = "15.01.2022"
        date_end = "20.01.2022"
        response_date_filter = self.client.get(url, {"date_begin": date_begin, "date_end": date_end})
        self.assertEqual(status.HTTP_200_OK, response_date_filter.status_code)
        queryset = Entrance.objects.filter(get_period_filter_lookup("date", date_begin, date_end))
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": EntranceListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_date_filter.data)

        # general_search
        response_general_search = self.client.get(url, {"general_search": "A-111"})
        self.assertEqual(status.HTTP_200_OK, response_general_search.status_code)
        queryset = Entrance.objects.filter(document_number="A-111")
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": EntranceListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_general_search.data)

    def test_create(self):
        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        payload = {
            "date": "18.10.2022",
            "document_number": "A-111",
            "responsible": responsible.pk,
            "provider": "ОАО КАМАЗ",
            "note": "Тестовое поступление",
            "turnovers_from_entrance": [
                {
                    "pk": None,
                    "date": "18.10.2022",
                    "material": material.pk,
                    "warehouse": warehouse.pk,
                    "price": 10.0,
                    "quantity": 2.0,
                    "sum": 20.0,
                }
            ],
        }

        url = reverse("entrance-list")
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Entrance.objects.get(document_number=payload["document_number"]))

    def test_get(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("entrance-detail", kwargs={"pk": entrance.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = EntranceSerializer(Entrance.objects.get(pk=entrance.pk)).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material1 = MaterialFactory(unit=unit, category=category)
        material2 = MaterialFactory(unit=unit, category=category, name="Масло моторное TOYOTA 5w20")

        warehouse1 = WarehouseFactory()
        warehouse2 = WarehouseFactory(name="Склад 2")

        responsible1 = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        responsible2 = EmployeeFactory(number_in_kadry=3, type=3, position="Техник")

        entrance = EntranceFactory(user=user, responsible=responsible1)
        turnover = TurnoverFactory(user=user, type=COMING, material=material1, warehouse=warehouse1, entrance=entrance)

        payload = {
            "pk": entrance.pk,
            "date": "01.01.2022",
            "document_number": "A-112",
            "responsible": responsible2.pk,
            "provider": "ГиперАвто",
            "note": "Тестовое поступление изменено",
            "turnovers_from_entrance": [
                {
                    "pk": turnover.pk,
                    "date": "02.01.2022",
                    "material": material2.pk,
                    "warehouse": warehouse2.pk,
                    "price": 15.00,
                    "quantity": 1.00,
                    "sum": 10.00,
                },
                {
                    "pk": None,
                    "date": "01.01.2022",
                    "material": material2.pk,
                    "warehouse": turnover.warehouse.pk,
                    "price": 5.00,
                    "quantity": 4.00,
                    "sum": 20.00,
                },
            ],
        }

        url = reverse("entrance-detail", kwargs={"pk": entrance.pk})
        response = self.client.put(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        changed_entrance = Entrance.objects.get(pk=entrance.pk)
        self.assertEqual(changed_entrance.date.strftime("%d.%m.%Y"), payload["date"])
        self.assertEqual(changed_entrance.document_number, payload["document_number"])
        self.assertEqual(changed_entrance.responsible.pk, payload["responsible"])
        self.assertEqual(changed_entrance.provider, payload["provider"])
        self.assertEqual(changed_entrance.note, payload["note"])

        turnovers_from_entrance = changed_entrance.turnovers_from_entrance.all().order_by("pk")
        self.assertNotEqual(
            turnovers_from_entrance[0].date.strftime("%d.%m.%Y"), payload["turnovers_from_entrance"][0]["date"]
        )
        self.assertNotEqual(turnovers_from_entrance[0].material.pk, payload["turnovers_from_entrance"][0]["material"])
        self.assertNotEqual(
            turnovers_from_entrance[0].warehouse.pk, payload["turnovers_from_entrance"][0]["warehouse"]
        )
        self.assertNotEqual(turnovers_from_entrance[0].price, payload["turnovers_from_entrance"][0]["price"])
        self.assertNotEqual(turnovers_from_entrance[0].quantity, payload["turnovers_from_entrance"][0]["quantity"])
        self.assertNotEqual(turnovers_from_entrance[0].sum, payload["turnovers_from_entrance"][0]["sum"])

        self.assertEqual(
            turnovers_from_entrance[1].date.strftime("%d.%m.%Y"), payload["turnovers_from_entrance"][1]["date"]
        )
        self.assertEqual(turnovers_from_entrance[1].material.pk, payload["turnovers_from_entrance"][1]["material"])
        self.assertEqual(turnovers_from_entrance[1].warehouse.pk, payload["turnovers_from_entrance"][1]["warehouse"])
        self.assertEqual(turnovers_from_entrance[1].price, payload["turnovers_from_entrance"][1]["price"])
        self.assertEqual(turnovers_from_entrance[1].quantity, payload["turnovers_from_entrance"][1]["quantity"])
        self.assertEqual(turnovers_from_entrance[1].sum, payload["turnovers_from_entrance"][1]["sum"])

    def test_delete_with_turnover(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("entrance-detail", kwargs={"pk": entrance.pk})

        with self.assertRaises(ProtectedError):
            response = self.client.delete(url)
            self.assertNotEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete(self):
        user = get_test_user()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)

        url = reverse("entrance-detail", kwargs={"pk": entrance.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Entrance.DoesNotExist):
            Entrance.objects.get(pk=entrance.pk)

    def test_get_providers(self):
        user = get_test_user()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance1 = EntranceFactory(user=user, responsible=responsible)
        entrance2 = EntranceFactory(user=user, responsible=responsible, provider="ГиперАвто")
        entrance3 = EntranceFactory(user=user, responsible=responsible)

        url = reverse("entrance-provider-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        result_providers = ["ГиперАвто", "ОАО КАМАЗ"]
        self.assertEqual(response.data, result_providers)
