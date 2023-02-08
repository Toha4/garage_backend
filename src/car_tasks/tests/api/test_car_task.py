import json

from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase
from app.helpers.testing import get_test_user
from core.tests.factory import CarFactory
from orders.constants import REQUEST
from orders.tests.factory import OrderFactory
from orders.tests.factory import PostFactory
from orders.tests.factory import ReasonFactory

from ...api.serializers import CarTaskListSerializer
from ...api.serializers import CarTaskSerializer
from ...models import CarTask
from ..factory import CarTaskFactory


class CarApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        user = get_test_user()
        car1 = CarFactory()
        car_task1 = CarTaskFactory(user=user, car=car1)
        car_task2 = CarTaskFactory(
            user=user,
            car=car1,
            description="Заменить лампу ДХО",
            materials="",
            is_completed=True,
            date_completed="2022-01-15",
        )

        car2 = CarFactory(kod_mar_in_putewka=2, gos_nom_in_putewka="666", state_number="А 666 АА", name="КАМАЗ 5000")
        car_task3 = CarTaskFactory(
            user=user, car=car2, description="Заменить левое заднее колесо, грыжа", materials=""
        )

        reason = ReasonFactory()
        post = PostFactory()

        order = OrderFactory(
            user=user,
            status=REQUEST,
            post=post,
            car=car2,
            date_begin="2022-01-01 12:00",
        )
        order.reasons.add(reason)

        car_task4 = CarTaskFactory(
            user=user,
            car=car2,
            description="Проверить масло",
            materials="",
            order=order,
            is_completed=True,
            date_completed="2022-01-15",
        )

        url = reverse("car-tasks-list")

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task3.pk, car_task1.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # car_filter
        response = self.client.get(url, {"car": car1.pk})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task1.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # show_completed_filter
        response = self.client.get(url, {"car": car1.pk, "show_completed": "true"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task2.pk, car_task1.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # order_created_filter
        response = self.client.get(url, {"car": car2.pk, "order_created": order.pk})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task4.pk, car_task3.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # description_search
        response = self.client.get(url, {"general_search": "колесо"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task3.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # materials_search
        response = self.client.get(url, {"general_search": "фильтр"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = CarTask.objects.filter(pk__in=[car_task1.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": CarTaskListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        car = CarFactory()

        payload = {
            "car": car.pk,
            "description": "Заменить воздушный фильтр",
            "materials": "Фильтр воздушеый арт. 0K6B023603",
            "is_completed": False,
        }

        url = reverse("car-tasks-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(CarTask.objects.get(description=payload["description"]))

    def test_get(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        url = reverse("car-tasks-detail", kwargs={"pk": car_task.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = CarTaskSerializer(CarTask.objects.get(pk=car_task.pk)).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        payload = {
            "pk": car_task.pk,
            "car": car.pk,
            "description": "Заменить лампу ДХО",
            "materials": "Лампа ДХО",
            "is_completed": True,
            "date_completed": "15.01.2022",
            "order": None,
        }
        url = reverse("car-tasks-detail", kwargs={"pk": car_task.pk})
        response = self.client.put(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        changed_car_task = CarTask.objects.get(pk=car_task.pk)
        self.assertEqual(changed_car_task.car.pk, payload["car"])
        self.assertEqual(changed_car_task.description, payload["description"])
        self.assertEqual(changed_car_task.materials, payload["materials"])
        self.assertEqual(changed_car_task.is_completed, payload["is_completed"])
        self.assertEqual(changed_car_task.date_completed.strftime("%d.%m.%Y"), payload["date_completed"])
        self.assertEqual(changed_car_task.order, payload["order"])

    def test_partial_update(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        payload = {
            "is_completed": True,
            "date_completed": "15.01.2022",
        }
        url = reverse("car-tasks-detail", kwargs={"pk": car_task.pk})
        response = self.client.put(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        changed_car_task = CarTask.objects.get(pk=car_task.pk)
        self.assertEqual(changed_car_task.is_completed, payload["is_completed"])
        self.assertEqual(changed_car_task.date_completed.strftime("%d.%m.%Y"), payload["date_completed"])

    def test_delete(self):
        user = get_test_user()
        car = CarFactory()
        car_task = CarTaskFactory(user=user, car=car)

        url = reverse("car-tasks-detail", kwargs={"pk": car_task.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(CarTask.DoesNotExist):
            CarTask.objects.get(pk=car_task.pk)
