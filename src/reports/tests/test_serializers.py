from django.test import TestCase

from core.tests.factory import EmployeeFactory

from ..api.serializers import EmployeeNoteSerializer
from .factory import EmployeeNoteFactory


class EmployeeNoteSerializerTestCase(TestCase):
    def test_ok(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        employee_note = EmployeeNoteFactory(employee=employee)
        data = EmployeeNoteSerializer(employee_note).data
        expected_data = {
            "pk": employee_note.pk,
            "employee": employee_note.employee.pk,
            "employee_short_fio": "Иванов И. И.",
            "date": "2022-01-01",
            "note": "Проявлял инициативу",
        }
        self.assertEqual(expected_data, data)
