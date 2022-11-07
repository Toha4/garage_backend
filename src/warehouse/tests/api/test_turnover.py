from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase
from app.helpers.testing import get_test_user
from core.tests.factory import CarFactory
from core.tests.factory import EmployeeFactory
from orders.constants import COMPLETED
from orders.constants import WORK
from orders.tests.factory import OrderFactory
from orders.tests.factory import PostFactory
from orders.tests.factory import ReasonFactory

from ...api.serializers import TurnoverMaterialReadSerializer
from ...api.serializers import TurnoverSerializer
from ...constants import COMING
from ...constants import EXPENSE
from ...models import Turnover
from ...tests.factory import EntranceFactory
from ...tests.factory import MaterialCategoryFactory
from ...tests.factory import MaterialFactory
from ...tests.factory import TurnoverFactory
from ...tests.factory import UnitFactory
from ...tests.factory import WarehouseFactory


class TurnoverApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material1 = MaterialFactory(unit=unit, category=category)
        material2 = MaterialFactory(unit=unit, category=category, name="Масло моторное TOYOTA 5w20")
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover1 = TurnoverFactory(user=user, type=COMING, material=material1, warehouse=warehouse, entrance=entrance)
        turnover2 = TurnoverFactory(
            user=user,
            type=COMING,
            material=material2,
            warehouse=warehouse,
            entrance=entrance,
            quantity=1.0,
            price=5.0,
            sum=5.0,
        )

        url = reverse("turnover-list")
        response = self.client.get(url, {"entrance_id": entrance.id})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Turnover.objects.filter(pk__in=[turnover1.pk, turnover2.pk])
        serializer_data = TurnoverSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        payload = {
            "type": COMING,
            "date": "18.10.2022",
            "is_correction": True,
            "note": "Тест корректировки",
            "user": user.id,
            "material": material.pk,
            "warehouse": warehouse.pk,
            "price": 10.00,
            "quantity": 2.0,
            "sum": 20.00,
        }

        url = reverse("turnover-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Turnover.objects.get(material_id=material.id))

    def test_get(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("turnover-detail", kwargs={"pk": turnover.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = TurnoverSerializer(Turnover.objects.get(pk=turnover.pk)).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        payload = {
            "pk": turnover.pk,
            "type": COMING,
            "date": "12.10.2022",
            "is_correction": True,
            "note": "Тест изменения корректировки",
            "user": user.id,
            "material": material.pk,
            "warehouse": warehouse.pk,
            "price": 5.00,
            "quantity": 2.0,
            "sum": 10.00,
        }

        url = reverse("turnover-detail", kwargs={"pk": entrance.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_delete_from_entrance(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        url = reverse("turnover-detail", kwargs={"pk": turnover.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_from_order_complited(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover_entrance = TurnoverFactory(
            user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance
        )

        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        order = OrderFactory(
            user=user,
            status=COMPLETED,
            reason=reason,
            post=post,
            car=car,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-15 08:00",
        )

        turnover_order = TurnoverFactory(user=user, type=EXPENSE, material=material, warehouse=warehouse, order=order)

        url = reverse("turnover-detail", kwargs={"pk": turnover_order.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_from_order_not_complited(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover_entrance = TurnoverFactory(
            user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance
        )

        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        order = OrderFactory(
            user=user,
            status=WORK,
            reason=reason,
            post=post,
            car=car,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-15 08:00",
        )

        turnover_order = TurnoverFactory(user=user, type=EXPENSE, material=material, warehouse=warehouse, order=order)

        url = reverse("turnover-detail", kwargs={"pk": turnover_order.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Turnover.DoesNotExist):
            Turnover.objects.get(pk=turnover_order.pk)

    def test_get_turnover_material_list(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover1 = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        warehouse2 = WarehouseFactory(name="Склад 2")
        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover2 = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse2, entrance=entrance)

        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        order = OrderFactory(
            user=user,
            status=WORK,
            reason=reason,
            post=post,
            car=car,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-01 08:00",
        )

        turnover3 = TurnoverFactory(user=user, type=EXPENSE, material=material, warehouse=warehouse, order=order)

        url = reverse("turnover-material-list")
        response = self.client.get(url, {"material_id": material.id})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Turnover.objects.filter(pk__in=[turnover1.pk, turnover2.pk, turnover3.pk]).order_by("-date", "-pk")
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 3,
            "page_size": 50,
            "results": TurnoverMaterialReadSerializer(queryset, many=True).data,
        }

        self.assertEqual(serializer_data, response.data)

        # warehouse_filter
        warehouse_filter = warehouse.id
        response_warehouse_filter = self.client.get(url, {"material_id": material.id, "warehouse": warehouse_filter})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Turnover.objects.filter(pk__in=[turnover1.pk, turnover3.pk]).order_by("-date", "-pk")
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": TurnoverMaterialReadSerializer(queryset, many=True).data,
        }

        self.assertEqual(serializer_data, response_warehouse_filter.data)

        # turnover_type_filter
        turnover_type = COMING
        response_warehouse_filter = self.client.get(url, {"material_id": material.id, "turnover_type": turnover_type})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Turnover.objects.filter(pk__in=[turnover1.pk, turnover2.pk]).order_by("-date", "-pk")
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": TurnoverMaterialReadSerializer(queryset, many=True).data,
        }

        self.assertEqual(serializer_data, response_warehouse_filter.data)

    def test_moving_material(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        warehouse2 = WarehouseFactory(name="Склад 2")

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        payload = {
            "material": material.id,
            "date": "01.01.2022",
            "warehouse_outgoing": warehouse.id,
            "warehouse_incoming": warehouse2.id,
            "price": 10.00,
            "quantity": 1.0,
            "sum": 10.00,
        }

        url = reverse("turnover-moving-material")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Turnover.objects.all().count(), 3)

    def test_moving_material_error(self):
        user = get_test_user()

        unit = UnitFactory()
        category = MaterialCategoryFactory()
        material = MaterialFactory(unit=unit, category=category)
        warehouse = WarehouseFactory()
        warehouse2 = WarehouseFactory(name="Склад 2")

        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")

        entrance = EntranceFactory(user=user, responsible=responsible)
        turnover = TurnoverFactory(user=user, type=COMING, material=material, warehouse=warehouse, entrance=entrance)

        payload = {
            "material": material.id,
            "date": "01.01.2022",
            "warehouse_outgoing": warehouse.id,
            "warehouse_incoming": warehouse2.id,
            "price": 10.00,
            "quantity": 3.0,
            "sum": 30.00,
        }

        url = reverse("turnover-moving-material")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotEqual(Turnover.objects.all().count(), 3)
