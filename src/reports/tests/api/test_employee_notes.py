from django.urls import reverse

from rest_framework import status

from app.helpers.testing import AuthorizationAPITestCase
from core.tests.factory import EmployeeFactory

from ...api.serializers import EmployeeNoteSerializer
from ...models import EmployeeNote
from ..factory import EmployeeNoteFactory


class EmployeeNoteApiTestCase(AuthorizationAPITestCase):
    def test_get_list(self):
        employee1 = EmployeeFactory(type=2, position="Слесарь")
        employee_note1 = EmployeeNoteFactory(employee=employee1)

        employee2 = EmployeeFactory(
            number_in_kadry=2,
            first_name="Александр",
            last_name="Александров",
            patronymic="Александрович",
            type=2,
            position="Слесарь",
        )
        employee_note2 = EmployeeNoteFactory(employee=employee2, note="Не пользовался СИЗ")

        url = reverse("reports-employee-notes-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        queryset = EmployeeNote.objects.filter(pk__in=[employee_note1.pk, employee_note2.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 2,
            "page_size": 50,
            "results": EmployeeNoteSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response.data)

        # general_search_fio
        search_fio = "Иванов"
        response_general_search_fio = self.client.get(url, {"general_search": search_fio})
        self.assertEqual(status.HTTP_200_OK, response_general_search_fio.status_code)
        queryset = EmployeeNote.objects.filter(pk__in=[employee_note1.pk])
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": EmployeeNoteSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_general_search_fio.data)

        # general_search_note
        search_note = "СИЗ"
        response_general_search_note = self.client.get(url, {"general_search": search_note})
        self.assertEqual(status.HTTP_200_OK, response_general_search_note.status_code)
        queryset = EmployeeNote.objects.filter(pk=employee_note2.pk)
        serializer_data = {
            "links": {"next": None, "previous": None},
            "numbers": {"current": 1, "previous": None, "next": None},
            "count": 1,
            "page_size": 50,
            "results": EmployeeNoteSerializer(queryset, many=True).data,
        }
        self.assertEqual(serializer_data, response_general_search_note.data)

    def test_create(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        payload = {
            "employee": employee.pk,
            "date": "15.11.2022",
            "note": "Проявлял инициативу",
        }

        url = reverse("reports-employee-notes-list")
        response = self.client.post(url, data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(EmployeeNote.objects.get(employee=employee))

    def test_get(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        employee_note = EmployeeNoteFactory(employee=employee)

        url = reverse("reports-employee-notes-detail", kwargs={"pk": employee_note.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        serializer_data = EmployeeNoteSerializer(EmployeeNote.objects.get(pk=employee_note.pk)).data
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        employee_note = EmployeeNoteFactory(employee=employee)

        payload = {"date": "16.11.2022", "note": "Не пользовался СИЗ"}

        url = reverse("reports-employee-notes-detail", kwargs={"pk": employee_note.pk})
        response = self.client.put(url, data=payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        employee_note_result = EmployeeNote.objects.get(pk=employee_note.pk)
        self.assertEqual(employee_note_result.date.strftime("%d.%m.%Y"), payload["date"])
        self.assertEqual(employee_note_result.note, payload["note"])

    def test_delete(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        employee_note = EmployeeNoteFactory(employee=employee)

        url = reverse("reports-employee-notes-detail", kwargs={"pk": employee_note.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(EmployeeNote.DoesNotExist):
            EmployeeNote.objects.get(pk=employee_note.pk)
