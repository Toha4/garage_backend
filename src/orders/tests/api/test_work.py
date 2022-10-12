from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import WorkListSerializer
from ...api.serializers import WorkSerializer
from ...models import Work
from ..factory import WorkCategoryFactory
from ..factory import WorkFactory


class WorkApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        work_category1 = WorkCategoryFactory()
        work_category2 = WorkCategoryFactory(name="ТО")
        work1 = WorkFactory(category=work_category1)
        work2 = WorkFactory(category=work_category2, name="Замена масла")
        work3 = WorkFactory(category=work_category2, name="Замена воздушного фильтра")

        url = reverse("work-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Work.objects.filter(pk__in=[work1.pk, work2.pk, work3.pk])
        serializer_data = WorkListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

        # category_filter
        response_category_filter = self.client.get(url, {"category": work_category2.pk})
        self.assertEqual(status.HTTP_200_OK, response_category_filter.status_code)
        queryset = Work.objects.filter(category=work_category2.pk)
        serializer_data = WorkListSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response_category_filter.data)

        # name_search
        response_name_search = self.client.get(url, {"search_name": "масла"})
        self.assertEqual(status.HTTP_200_OK, response_name_search.status_code)
        serializer_data = WorkListSerializer([work2], many=True).data
        self.assertEqual(serializer_data, response_name_search.data)

    def test_create(self):
        work_category = WorkCategoryFactory()

        payload = {"name": "Замена аккумулятора", "category": work_category.pk}

        url = reverse("work-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Work.objects.get(name=payload["name"]))

    def test_get(self):
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)

        url = reverse("work-detail", kwargs={"pk": work.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = WorkSerializer(work).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        work_category1 = WorkCategoryFactory()
        work_category2 = WorkCategoryFactory(name="ТО")

        work = WorkFactory(category=work_category1)
        payload = {"name": "Замена масла", "category": work_category2.pk}

        url = reverse("work-detail", kwargs={"pk": work.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        work_result = Work.objects.get(pk=work.pk)
        self.assertEqual(work_result.name, payload["name"])
        self.assertEqual(work_result.category.pk, payload["category"])

    def test_delete(self):
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)

        url = reverse("work-detail", kwargs={"pk": work.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Work.DoesNotExist):
            Work.objects.get(pk=work.pk)
