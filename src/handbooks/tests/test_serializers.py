from django.test import TestCase

from handbooks.api.serializers import CarDetailSerializer
from handbooks.api.serializers import CarShortSerializer
from handbooks.api.serializers import EmployeeDetailSerializer
from handbooks.api.serializers import EmployeeShortSerializer
from handbooks.api.serializers import PostSerializer
from handbooks.api.serializers import ReasonSerializer
from handbooks.models import Car
from handbooks.models import Employee
from handbooks.models import Post
from handbooks.models import Reason


class ReasonSerializerTestCase(TestCase):
    def test_ok(self):
        reason = Reason.objects.create(name="ТО", type=1)
        data = ReasonSerializer(reason).data
        expected_data = {
            "pk": reason.pk,
            "name": "ТО",
            "type": 1,
        }
        self.assertEqual(expected_data, data)


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        post = Post.objects.create(name="Бокс 1")
        data = PostSerializer(post).data
        expected_data = {
            "pk": post.pk,
            "name": "Бокс 1",
        }
        self.assertEqual(expected_data, data)


class CarSerializerTestCase(TestCase):
    def test_short(self):
        car = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )
        data = CarShortSerializer(car).data
        expected_data = {"pk": car.pk, "state_number": "А 777 АА", "name": "УАЗ 123"}
        self.assertEqual(expected_data, data)

    def test_detail(self):
        car = Car.objects.create(
            kod_mar_in_putewka=1,
            gos_nom_in_putewka="777",
            state_number="А 777 АА",
            name="УАЗ 123",
            kod_driver=11,
            date_decommissioned=None,
        )
        data = CarDetailSerializer(car).data
        expected_data = {
            "pk": car.pk,
            "kod_mar_in_putewka": 1,
            "gos_nom_in_putewka": "777",
            "state_number": "А 777 АА",
            "name": "УАЗ 123",
            "kod_driver": 11,
            "date_decommissioned": None,
        }
        self.assertEqual(expected_data, data)


class EmployeeSerializerTestCase(TestCase):
    def test_short(self):
        employee = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )
        data = EmployeeShortSerializer(employee).data
        expected_data = {"pk": employee.pk, "short_fio": "Иванов И. И.", "type": 2}
        self.assertEqual(expected_data, data)

    def test_detail(self):
        employee = Employee.objects.create(
            number_in_kadry=1,
            first_name="Иван",
            last_name="Иванов",
            patronymic="Иванович",
            type=2,
            position="Слесарь 1 раз.",
            date_dismissal=None,
        )
        data = EmployeeDetailSerializer(employee).data
        expected_data = {
            "pk": employee.pk,
            "number_in_kadry": 1,
            "short_fio": "Иванов И. И.",
            "first_name": "Иван",
            "last_name": "Иванов",
            "patronymic": "Иванович",
            "type": 2,
            "position": "Слесарь 1 раз.",
            "date_dismissal": None,
        }
        self.assertEqual(expected_data, data)
