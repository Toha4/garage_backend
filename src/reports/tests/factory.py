from factory.django import DjangoModelFactory

from ..models import EmployeeNote


class EmployeeNoteFactory(DjangoModelFactory):
    employee = None
    date = "2022-01-01"
    note = "Проявлял инициативу"

    class Meta:
        model = EmployeeNote
