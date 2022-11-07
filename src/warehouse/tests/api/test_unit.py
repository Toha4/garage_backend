from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import UnitSerializer
from ...models import Unit
from ..factory import UnitFactory


class UnitApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        unit1 = UnitFactory()
        unit2 = UnitFactory(name="шт")

        url = reverse("unit-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Unit.objects.filter(pk__in=[unit1.pk, unit2.pk])
        serializer_data = UnitSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "кг", "is_precision_point": True}

        url = reverse("unit-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Unit.objects.get(name=payload["name"]))

    def test_get(self):
        unit = UnitFactory()

        url = reverse("unit-detail", kwargs={"pk": unit.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = UnitSerializer(unit).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        unit = UnitFactory()
        payload = {"name": "шт", "is_precision_point": False}

        url = reverse("unit-detail", kwargs={"pk": unit.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        unit_result = Unit.objects.get(pk=unit.pk)
        self.assertEqual(unit_result.name, payload["name"])

    def test_delete(self):
        unit = UnitFactory()

        url = reverse("unit-detail", kwargs={"pk": unit.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Unit.DoesNotExist):
            Unit.objects.get(pk=unit.pk)
