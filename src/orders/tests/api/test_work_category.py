from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import WorkCategorySerializer
from ...models import WorkCategory
from ..factory import WorkCategoryFactory


class WorkCategoryApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        work_category1 = WorkCategoryFactory()
        work_category2 = WorkCategoryFactory(name="Ходовая")

        url = reverse("work-category-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = WorkCategory.objects.filter(pk__in=[work_category1.pk, work_category2.pk])
        serializer_data = WorkCategorySerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "Электрика"}

        url = reverse("work-category-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(WorkCategory.objects.get(name=payload["name"]))

    def test_get(self):
        work_category = WorkCategoryFactory()

        url = reverse("work-category-detail", kwargs={"pk": work_category.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = WorkCategorySerializer(work_category).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        work_category = WorkCategoryFactory()
        payload = {"name": "Ходовая"}

        url = reverse("work-category-detail", kwargs={"pk": work_category.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        work_category_result = WorkCategory.objects.get(pk=work_category.pk)
        self.assertEqual(work_category_result.name, payload["name"])

    def test_delete(self):
        work_category = WorkCategoryFactory()

        url = reverse("work-category-detail", kwargs={"pk": work_category.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(WorkCategory.DoesNotExist):
            WorkCategory.objects.get(pk=work_category.pk)
