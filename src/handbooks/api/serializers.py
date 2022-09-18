from django.conf import settings

from rest_framework.serializers import DateField
from rest_framework.serializers import ModelSerializer

from ..models import Car
from ..models import Employee
from ..models import Post
from ..models import Reason


class ReasonSerializer(ModelSerializer):
    class Meta:
        model = Reason
        fields = (
            "pk",
            "name",
            "type",
        )


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "pk",
            "name",
        )


class CarShortSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "pk",
            "state_number",
            "name",
        )


class CarDetailSerializer(ModelSerializer):
    date_decommissioned = DateField(**settings.SERIALIZER_DATE_PARAMS, required=False, allow_null=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            "pk",
            "kod_mar_in_putewka",
            "gos_nom_in_putewka",
            "state_number",
            "name",
            "kod_driver",
            "date_decommissioned",
        )
        read_only_fields = (
            "pk",
            "kod_mar_in_putewka",
            "gos_nom_in_putewka",
            "state_number",
            "kod_driver",
            "date_decommissioned",
        )


class EmployeeShortSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "pk",
            "short_fio",
            "type",
        )


class EmployeeDetailSerializer(ModelSerializer):
    date_dismissal = DateField(**settings.SERIALIZER_DATE_PARAMS, required=False, allow_null=True, read_only=True)

    class Meta:
        model = Employee
        fields = (
            "pk",
            "number_in_kadry",
            "short_fio",
            "first_name",
            "last_name",
            "patronymic",
            "type",
            "position",
            "date_dismissal",
        )
        read_only_fields = (
            "pk",
            "number_in_kadry",
            "first_name",
            "last_name",
            "patronymic",
            "position",
            "date_dismissal",
        )
