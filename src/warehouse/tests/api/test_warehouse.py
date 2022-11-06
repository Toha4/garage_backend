from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import WarehouseListSerializer
from ...api.serializers import WarehouseSerializer
from ...models import Warehouse
from ..factory import WarehouseFactory


class WarehouseApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        warehouse1 = WarehouseFactory()
        warehouse2 = WarehouseFactory(name="Склад 2")

        url = reverse("warehouse-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Warehouse.objects.filter(pk__in=[warehouse1.pk, warehouse2.pk])
        serializer_data = WarehouseListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "Главный склад"}

        url = reverse("warehouse-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Warehouse.objects.get(name=payload["name"]))

    def test_get(self):
        warehouse = WarehouseFactory()

        url = reverse("warehouse-detail", kwargs={"pk": warehouse.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = WarehouseSerializer(warehouse).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        warehouse = WarehouseFactory()
        payload = {"name": "Склад 2"}

        url = reverse("warehouse-detail", kwargs={"pk": warehouse.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        warehouse_result = Warehouse.objects.get(pk=warehouse.pk)
        self.assertEqual(warehouse_result.name, payload["name"])

    def test_delete(self):
        warehouse = WarehouseFactory()

        url = reverse("warehouse-detail", kwargs={"pk": warehouse.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Warehouse.DoesNotExist):
            Warehouse.objects.get(pk=warehouse.pk)
