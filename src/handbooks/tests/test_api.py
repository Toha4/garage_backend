from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ..api.serializers import CarDetailSerializer
from ..api.serializers import CarShortSerializer
from ..api.serializers import EmployeeDetailSerializer
from ..api.serializers import EmployeeShortSerializer
from ..api.serializers import PostSerializer
from ..api.serializers import ReasonSerializer
from ..models import Car
from ..models import Employee
from ..models import Post
from ..models import Reason


class ReasonApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        reason1 = Reason.objects.create(name="ТО", type=1)
        reason2 = Reason.objects.create(name="Ремонт", type=2)
        reason3 = Reason.objects.create(name="Прочее", type=3)

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
        reason = Reason.objects.create(name="ТО", type=1)

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = ReasonSerializer(reason).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        reason = Reason.objects.create(name="ТО", type=1)
        payload = {"name": "Ремонт", "type": 2}

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        reason_result = Reason.objects.get(pk=reason.pk)
        self.assertEqual(reason_result.name, payload["name"])
        self.assertEqual(reason_result.type, payload["type"])

    def test_delete(self):
        reason = Reason.objects.create(name="ТО", type=1)

        url = reverse("reason-detail", kwargs={"pk": reason.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Reason.DoesNotExist):
            Reason.objects.get(pk=reason.pk)


class PostApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        post1 = Post.objects.create(name="Бокс 1")
        post2 = Post.objects.create(name="Бокс 2")

        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Post.objects.filter(pk__in=[post1.pk, post2.pk])
        serializer_data = PostSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        payload = {"name": "Бокс 1"}

        url = reverse("post-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Post.objects.get(name=payload["name"]))

    def test_get(self):
        post = Post.objects.create(name="Бокс 1")

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = PostSerializer(post).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        post = Post.objects.create(name="Бокс 1")
        payload = {"name": "Бокс 2"}

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        post_result = Post.objects.get(pk=post.pk)
        self.assertEqual(post_result.name, payload["name"])

    def test_delete(self):
        post = Post.objects.create(name="Бокс 1")

        url = reverse("post-detail", kwargs={"pk": post.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post.pk)


class CarApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        car1 = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )
        car2 = Car.objects.create(
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
            "name": "УАЗ 123",
            "kod_driver": 11,
            "date_decommissioned": "01.01.2022",
        }

        url = reverse("car-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_get(self):
        car = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )

        url = reverse("car-detail", kwargs={"pk": car.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = CarDetailSerializer(car).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        car = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )
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
        car = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )

        url = reverse("car-detail", kwargs={"pk": car.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        try:
            Car.objects.get(pk=car.pk)
        except Car.DoesNotExist:
            self.fail("Car.objects.get raised Car.DoesNotExist unexpectedly!")


class EmployeeApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        employee1 = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal="2022-01-01",
        )
        employee2 = Employee.objects.create(
            number_in_kadry=2,
            first_name="Антон",
            last_name="Антонов",
            patronymic="Антонович",
            type=3,
            position="Начальник",
            date_dismissal=None,
        )

        url = reverse("employee-list")
        response = self.client.get(url, {"show_dismissal": "True"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Employee.objects.filter(pk__in=[employee1.pk, employee2.pk])
        serializer_data = EmployeeShortSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

        # type_filter
        response_type_filter = self.client.get(url, {"show_dismissal": "True", "type": 3})
        self.assertEqual(status.HTTP_200_OK, response_type_filter.status_code)
        serializer_data = EmployeeShortSerializer([employee2], many=True).data
        self.assertEqual(serializer_data, response_type_filter.data)

        # fio_search
        response_fio_search = self.client.get(url, {"show_dismissal": "True", "fio_search": "Иван"})
        self.assertEqual(status.HTTP_200_OK, response_fio_search.status_code)
        serializer_data = EmployeeShortSerializer([employee1], many=True).data
        self.assertEqual(serializer_data, response_fio_search.data)

    def test_create_forbidden(self):
        payload = {
            "number_in_kadry": 1,
            "first_name": "Иван",
            "last_name": "Иванов",
            "patronymic": "Иванович",
            "type": 2,
            "position": "Слесарь 1 раз.",
            "date_dismissal": "01.01.2022",
        }

        url = reverse("employee-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_get(self):
        employee = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )

        url = reverse("employee-detail", kwargs={"pk": employee.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = EmployeeDetailSerializer(employee).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        employee = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )
        payload = {
            "number_in_kadry": 2,
            "first_name": "Антон",
            "last_name": "Антонов",
            "patronymic": "Антонович",
            "type": 3,
            "position": "Начальник",
            "date_dismissal": "01.01.2022",
        }

        url = reverse("employee-detail", kwargs={"pk": employee.pk})

        response_put = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response_put.status_code)

        response_patch = self.client.patch(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response_patch.status_code)

        employee_result = Employee.objects.get(pk=employee.pk)
        self.assertEqual(employee_result.type, payload["type"])
        self.assertNotEqual(employee_result.number_in_kadry, payload["number_in_kadry"])
        self.assertNotEqual(employee_result.first_name, payload["first_name"])
        self.assertNotEqual(employee_result.last_name, payload["last_name"])
        self.assertNotEqual(employee_result.patronymic, payload["patronymic"])
        self.assertNotEqual(employee_result.position, payload["position"])
        self.assertNotEqual(employee_result.date_dismissal, payload["date_dismissal"])

    def test_delete_forbidden(self):
        employee = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )

        url = reverse("employee-detail", kwargs={"pk": employee.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        try:
            Employee.objects.get(pk=employee.pk)
        except Employee.DoesNotExist:
            self.fail("Employee.objects.get raised Employee.DoesNotExist unexpectedly!")
