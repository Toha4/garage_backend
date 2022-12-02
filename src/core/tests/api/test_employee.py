from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase

from ...api.serializers import EmployeeDetailSerializer
from ...api.serializers import EmployeeShortSerializer
from ...models import Employee
from ..factory import EmployeeFactory


class EmployeeApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        employee1 = EmployeeFactory()
        employee2 = EmployeeFactory(
            number_in_kadry=2,
            first_name="Антон",
            last_name="Антонов",
            patronymic="Антонович",
            type=3,
            position="Начальник",
            date_dismissal="2022-01-01",
        )

        url = reverse("employee-list")
        response = self.client.get(url, {"show_dismissal": "True"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = Employee.objects.filter(pk__in=[employee1.pk, employee2.pk])
        serializer_data = EmployeeShortSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response.data)

        # date_request_filter
        response_date_request_filter = self.client.get(url, {"date_request": "01.01.2022"})
        self.assertEqual(status.HTTP_200_OK, response_date_request_filter.status_code)
        serializer_data = EmployeeShortSerializer(queryset, many=True).data
        self.assertEqual(serializer_data, response_date_request_filter.data)

        # type_filter
        response_type_filter = self.client.get(url, {"show_dismissal": "True", "types": "3"})
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
        employee = EmployeeFactory()

        url = reverse("employee-detail", kwargs={"pk": employee.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = EmployeeDetailSerializer(employee).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        employee = EmployeeFactory()
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
        employee = EmployeeFactory()

        url = reverse("employee-detail", kwargs={"pk": employee.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        try:
            Employee.objects.get(pk=employee.pk)
        except Employee.DoesNotExist:
            self.fail("Employee.objects.get raised Employee.DoesNotExist unexpectedly!")
