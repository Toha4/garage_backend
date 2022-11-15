from django.db.models import PROTECT
from django.test import TestCase

from core.tests.factory import EmployeeFactory

from .factory import EmployeeNoteFactory


class EmployeeNoteModelTestCase(TestCase):
    def setUp(self):
        employee = EmployeeFactory(type=2, position="Слесарь")
        self.employee_note = EmployeeNoteFactory(employee=employee)

    def test_fields(self):
        employee_null = self.employee_note._meta.get_field("employee").null
        self.assertEqual(employee_null, False)

        employee_on_delete = self.employee_note._meta.get_field("employee").remote_field.on_delete
        self.assertEqual(employee_on_delete, PROTECT)

        date_null = self.employee_note._meta.get_field("date").null
        self.assertEqual(date_null, False)

        note_null = self.employee_note._meta.get_field("note").null
        self.assertEqual(note_null, False)
