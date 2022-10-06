import copy
import json

from django.urls import reverse

from rest_framework import status

from app.helpers.database import convert_to_localtime
from app.helpers.database import get_period_filter_lookup
from app.helpers.testing import AuthorizationAPITestCase
from core.tests.factory import CarFactory
from core.tests.factory import EmployeeFactory
from orders.helpers.order_general_search import order_general_search

from ...api.serializers import OrderDetailSerializer
from ...api.serializers import OrderListSerializer
from ...constants import COMPLETED
from ...constants import REQUEST
from ...models import Order
from ..factory import OrderFactory
from ..factory import PostFactory
from ..factory import ReasonFactory
from ..factory import WorkCategoryFactory
from ..factory import WorkFactory


class OrderApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        reason1 = ReasonFactory()
        reason2 = ReasonFactory(type=2, name="Ремонт электрооборудования")
        post = PostFactory()
        car1 = CarFactory()
        car2 = CarFactory(gos_nom_in_putewka=2, name="КАМАЗ", state_number="Б 666 ББ")
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order1 = OrderFactory(
            status=REQUEST,
            reason=reason1,
            post=post,
            car=car1,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-01 12:00",
        )
        order2 = OrderFactory(
            status=COMPLETED,
            reason=reason1,
            post=post,
            car=car1,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-15 08:00",
        )
        order3 = OrderFactory(
            status=COMPLETED,
            reason=reason2,
            post=post,
            car=car2,
            driver=driver,
            responsible=responsible,
            date_begin="2022-01-17 08:00",
            note="Поломка",
        )

        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Order.objects.filter(pk__in=[order1.pk, order2.pk, order3.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 3,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # reason_type_filter
        response_reasons_filter = self.client.get(url, {"reason_type": reason1.type})
        self.assertEqual(status.HTTP_200_OK, response_reasons_filter.status_code)
        queryset = Order.objects.filter(reason__type__in=[reason1.type])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_reasons_filter.data)

        # status_filter
        response_status_filter = self.client.get(url, {"statuses": ",".join(str(i) for i in[COMPLETED,])})
        self.assertEqual(status.HTTP_200_OK, response_status_filter.status_code)
        queryset = Order.objects.filter(status__in=[COMPLETED])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_status_filter.data)

        # date_filter
        date_begin = "15.01.2022"
        date_end = "20.01.2022"
        response_date_filter = self.client.get(url, {"date_begin": date_begin, "date_end": date_end})
        self.assertEqual(status.HTTP_200_OK, response_date_filter.status_code)
        queryset = Order.objects.filter(get_period_filter_lookup("date_begin", date_begin, date_end, True))
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_date_filter.data)

        # number_searsh
        number = str(order3.number)
        response_number_search = self.client.get(url, {"general_search": number})
        self.assertEqual(status.HTTP_200_OK, response_number_search.status_code)
        queryset = order_general_search(Order.objects.all(), number)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_number_search.data)

        # car_state_number_search
        car_state_number = "Б666ББ"
        response_car_state_number_search = self.client.get(url, {"general_search": car_state_number})
        self.assertEqual(status.HTTP_200_OK, response_car_state_number_search.status_code)
        queryset = order_general_search(Order.objects.all(), car_state_number)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_car_state_number_search.data)

        # car_name_search
        car_name = "камаз"
        response_car_name_search = self.client.get(url, {"general_search": car_name})
        self.assertEqual(status.HTTP_200_OK, response_car_name_search.status_code)
        queryset = order_general_search(Order.objects.all(), car_name)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_car_name_search.data)

        # reason_name_search
        reason_name = "Ремонт электрооборудования"
        response_reason_name_search = self.client.get(url, {"general_search": reason_name})
        self.assertEqual(status.HTTP_200_OK, response_reason_name_search.status_code)
        queryset = order_general_search(Order.objects.all(), reason_name)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_reason_name_search.data)

        # note_search
        note = "Поломка"
        response_note_search = self.client.get(url, {"general_search": note})
        self.assertEqual(status.HTTP_200_OK, response_note_search.status_code)
        queryset = order_general_search(Order.objects.all(), note)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": OrderListSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_note_search.data)

    def test_create(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        work_category = WorkCategoryFactory()
        work = WorkFactory(category=work_category)
        mechanic = EmployeeFactory(number_in_kadry=3, type=2, position="Слесарь")

        url = reverse("order-list")

        # Order only
        payload = {
            "status": REQUEST,
            "reason": reason.pk,
            "date_begin": "19.09.2022 12:00",
            "date_end": None,
            "post": post.pk,
            "car": car.pk,
            "driver": driver.pk,
            "responsible": responsible.pk,
            "odometer": 123000,
            "note": "Тестовый заказ-наряд 1",
            "order_works": [],
        }

        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Order.objects.get(note=payload["note"]))

        # Order with works
        payload_with_works = copy.copy(payload)
        payload_with_works["order_works"] = [
            {
                "pk": None,
                "work": work.pk,
                "quantity": 1,
                "time_minutes": 120,
                "note": "Тестовая работа",
                "mechanics": [],
            }
        ]
        payload_with_works["note"] = "Тестовый заказ-наряд 2"
        response = self.client.post(url, data=json.dumps(payload_with_works), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Order.objects.get(note=payload_with_works["note"]))

        # Order with duplicate works
        payload_with_works_duplicate = copy.copy(payload)
        payload_with_works_duplicate["order_works"] = [
            {
                "pk": None,
                "work": work.pk,
                "quantity": 1,
                "time_minutes": 120,
                "note": "Тестовая работа",
                "mechanics": [],
            },
            {
                "pk": None,
                "work": work.pk,
                "quantity": 1,
                "time_minutes": 120,
                "note": "Тестовая работа",
                "mechanics": [],
            },
        ]
        payload_with_works_duplicate["note"] = "Тестовый заказ-наряд 3"
        response = self.client.post(
            url, data=json.dumps(payload_with_works_duplicate), content_type="application/json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(note=payload_with_works_duplicate["note"])

        # Order with works and mechanics
        payload_with_works_mechanics = copy.copy(payload)
        payload_with_works_mechanics["order_works"] = [
            {
                "pk": None,
                "work": work.pk,
                "quantity": 1,
                "time_minutes": 120,
                "note": "Тестовая работа",
                "mechanics": [{"pk": None, "mechanic": mechanic.pk, "time_minutes": 60}],
            }
        ]
        payload_with_works_mechanics["note"] = "Тестовый заказ-наряд 4"
        response = self.client.post(
            url, data=json.dumps(payload_with_works_mechanics), content_type="application/json"
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Order.objects.get(note=payload_with_works_mechanics["note"]))

        # Order with works and duplicate mechanics
        payload_with_works_mechanics_duplicate = copy.copy(payload)
        payload_with_works_mechanics_duplicate["order_works"] = [
            {
                "pk": None,
                "work": work.pk,
                "quantity": 1,
                "time_minutes": 120,
                "note": "Тестовая работа",
                "mechanics": [
                    {"pk": None, "mechanic": mechanic.pk, "time_minutes": 60},
                    {"pk": None, "mechanic": mechanic.pk, "time_minutes": 60},
                ],
            }
        ]
        payload_with_works_mechanics_duplicate["note"] = "Тестовый заказ-наряд 5"
        response = self.client.post(
            url, data=json.dumps(payload_with_works_mechanics_duplicate), content_type="application/json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(note=payload_with_works_mechanics_duplicate["note"])

    def test_get(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(reason=reason, post=post, car=car, driver=driver, responsible=responsible)

        url = reverse("order-detail", kwargs={"pk": order.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = OrderDetailSerializer(Order.objects.get(pk=order.pk)).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        reason1 = ReasonFactory()
        reason2 = ReasonFactory(name="TO2")
        post1 = PostFactory()
        post2 = PostFactory(name="Бокс 2")
        car1 = CarFactory()
        car2 = CarFactory(
            kod_mar_in_putewka=2,
            gos_nom_in_putewka="666",
            state_number="Б 666 ББ",
            name="КАМАЗ 321",
            kod_driver=12,
            date_decommissioned="2022-01-01",
        )
        driver1 = EmployeeFactory(type=1, position="Водитель")
        driver2 = EmployeeFactory(number_in_kadry=2, type=1, position="Водитель 2")
        responsible1 = EmployeeFactory(number_in_kadry=3, type=3, position="Начальник")
        responsible2 = EmployeeFactory(number_in_kadry=4, type=3, position="Начальник 2")
        order = OrderFactory(reason=reason1, post=post1, car=car1, driver=driver1, responsible=responsible1)

        payload = {
            "number": 2,
            "status": COMPLETED,
            "reason": reason2.pk,
            "date_begin": "19.09.2022 14:00",
            "date_end": "20.09.2022 17:00",
            "post": post2.pk,
            "car": car2.pk,
            "driver": driver2.pk,
            "responsible": responsible2.pk,
            "odometer": 321000,
            "note": "Тестовый заказ-наряд 321",
        }

        url = reverse("order-detail", kwargs={"pk": order.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        reason_result = Order.objects.get(pk=order.pk)
        self.assertNotEqual(reason_result.number, payload["number"])
        self.assertEqual(reason_result.status, payload["status"])
        self.assertEqual(reason_result.reason.pk, payload["reason"])
        self.assertEqual(
            convert_to_localtime(reason_result.date_begin).strftime("%d.%m.%Y %H:%M"), payload["date_begin"]
        )
        self.assertEqual(convert_to_localtime(reason_result.date_end).strftime("%d.%m.%Y %H:%M"), payload["date_end"])
        self.assertEqual(reason_result.post.pk, payload["post"])
        self.assertEqual(reason_result.car.pk, payload["car"])
        self.assertEqual(reason_result.driver.pk, payload["driver"])
        self.assertEqual(reason_result.responsible.pk, payload["responsible"])
        self.assertEqual(reason_result.odometer, payload["odometer"])
        self.assertEqual(reason_result.note, payload["note"])

    def test_delete(self):
        reason = ReasonFactory()
        post = PostFactory()
        car = CarFactory()
        driver = EmployeeFactory(type=1, position="Водитель")
        responsible = EmployeeFactory(number_in_kadry=2, type=3, position="Начальник")
        order = OrderFactory(reason=reason, post=post, car=car, driver=driver, responsible=responsible)

        url = reverse("order-detail", kwargs={"pk": order.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=order.pk)
