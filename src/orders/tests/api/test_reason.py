from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import ReasonSerializer
from ...models import Reason
from ..factory import ReasonFactory


class ReasonApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        reason1 = ReasonFactory()
        reason2 = ReasonFactory(name="Ремонт", type=2)
        reason3 = ReasonFactory(name="Прочее", type=3)

        url = reverse("reason-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Reason.objects.filter(pk__in=[reason1.pk, reason2.pk, reason3.pk])
        serializer_data = ReasonSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "TO", "type": 1}

        url = reverse("reason-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Reason.objects.get(name=payload["name"]))

    def test_get(self):
        reason = ReasonFactory()

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = ReasonSerializer(reason).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        reason = ReasonFactory()
        payload = {"name": "Ремонт", "type": 2}

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        reason_result = Reason.objects.get(pk=reason.pk)
        self.assertEqual(reason_result.name, payload["name"])
        self.assertEqual(reason_result.type, payload["type"])

    def test_delete(self):
        reason = ReasonFactory(name="ТО", type=1)

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Reason.DoesNotExist):
            Reason.objects.get(pk=reason.pk)
