from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import MaterialCategoryListSerializer
from ...api.serializers import MaterialCategorySerializer
from ...models import MaterialCategory
from ..factory import MaterialCategoryFactory


class MaterialCategoryApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        material_category1 = MaterialCategoryFactory()
        material_category2 = MaterialCategoryFactory(name="шт")

        url = reverse("material-category-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = MaterialCategory.objects.filter(pk__in=[material_category1.pk, material_category2.pk])
        serializer_data = MaterialCategoryListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "Фильтра"}

        url = reverse("material-category-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(MaterialCategory.objects.get(name=payload["name"]))

    def test_get(self):
        material_category = MaterialCategoryFactory()

        url = reverse("material-category-detail", kwargs={"pk": material_category.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = MaterialCategorySerializer(material_category).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        material_category = MaterialCategoryFactory()
        payload = {"name": "Фильтра"}

        url = reverse("material-category-detail", kwargs={"pk": material_category.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        material_category_result = MaterialCategory.objects.get(pk=material_category.pk)
        self.assertEqual(material_category_result.name, payload["name"])

    def test_delete(self):
        material_category = MaterialCategoryFactory()

        url = reverse("material-category-detail", kwargs={"pk": material_category.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(MaterialCategory.DoesNotExist):
            MaterialCategory.objects.get(pk=material_category.pk)
