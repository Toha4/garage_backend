from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import CarDetailSerializer
from ...api.serializers import CarShortSerializer
from ...models import Car
from ..factory import CarFactory


class CarApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        car1 = CarFactory()
        car2 = CarFactory(
            kod_mar_in_putewka=2,
            gos_nom_in_putewka="666",
            state_number="Б 666 ББ",
            name="КАМАЗ 321",
            kod_driver=12,
            date_decommissioned="2022-01-01",
        )

        url = reverse("car-list")

        response = self.client.get(url, {"show_decommissioned": "True"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Car.objects.filter(pk__in=[car1.pk, car2.pk])
        serializer_data = CarShortSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

        # state_number_search
        response_state_number_search = self.client.get(
            url, {"show_decommissioned": "True", "state_number_search": "666"}
        )
        self.assertEqual(status.HTTP_200_OK, response_state_number_search.status_code)
        serializer_data = CarShortSerializer([car2], many=True).data
        self.assertEqual(serializer_data, response_state_number_search.data)

        # name_search
        response_name_search = self.client.get(url, {"show_decommissioned": "True", "name_search": "УАЗ"})
        self.assertEqual(status.HTTP_200_OK, response_name_search.status_code)
        serializer_data = CarShortSerializer([car1], many=True).data
        self.assertEqual(serializer_data, response_name_search.data)

    def test_create_forbidden(self):
        payload = {
            "kod_mar_in_putewka": 1,
            "gos_nom_in_putewka": "222",
            "state_number": "А 777 АА",
            "name": "УАЗ 111",
            "kod_driver": 11,
            "date_decommissioned": "01.01.2022",
        }

        url = reverse("car-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_get(self):
        car = CarFactory()

        url = reverse("car-detail", kwargs={"pk": car.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = CarDetailSerializer(car).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        car = CarFactory()
        payload = {
            "kod_mar_in_putewka": 2,
            "gos_nom_in_putewka": "666",
            "state_number": "Б 666 ББ",
            "name": "КАМАЗ 321",
            "kod_driver": 12,
            "date_decommissioned": "01.01.2022",
        }

        url = reverse("car-detail", kwargs={"pk": car.pk})

        response_put = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response_put.status_code)

        response_patch = self.client.patch(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response_patch.status_code)

        car_result = Car.objects.get(pk=car.pk)
        self.assertEqual(car_result.name, payload["name"])
        self.assertNotEqual(car_result.kod_mar_in_putewka, payload["kod_mar_in_putewka"])
        self.assertNotEqual(car_result.gos_nom_in_putewka, payload["gos_nom_in_putewka"])
        self.assertNotEqual(car_result.state_number, payload["state_number"])
        self.assertNotEqual(car_result.kod_driver, payload["kod_driver"])
        self.assertNotEqual(car_result.date_decommissioned, payload["date_decommissioned"])

    def test_delete_forbidden(self):
        car = CarFactory()

        url = reverse("car-detail", kwargs={"pk": car.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        try:
            Car.objects.get(pk=car.pk)
        except Car.DoesNotExist:
            self.fail("Car.objects.get raised Car.DoesNotExist unexpectedly!")
