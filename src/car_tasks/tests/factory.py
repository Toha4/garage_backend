from factory.django import DjangoModelFactory

from ..models import CarTask


class CarTaskFactory(DjangoModelFactory):
    user = None
    car = None
    description = "Заменить воздушный фильтр"
    materials = "Фильтр воздушеый арт. 0K6B023603"
    is_completed = False
    date_completed = None
    order = None

    class Meta:
        model = CarTask
