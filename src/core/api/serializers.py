from django.conf import settings

from rest_framework.serializers import DateField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from warehouse.helpers.material_utils import has_tag_materials

from ..models import Car
from ..models import Employee


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
    driver_pk = SerializerMethodField()
    has_tag_material = SerializerMethodField()
    car_task_count = SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "pk",
            "kod_mar_in_putewka",
            "gos_nom_in_putewka",
            "state_number",
            "name",
            "kod_driver",
            "driver_pk",
            "date_decommissioned",
            "has_tag_material",
            "car_task_count",
        )
        read_only_fields = (
            "pk",
            "kod_mar_in_putewka",
            "gos_nom_in_putewka",
            "state_number",
            "kod_driver",
            "date_decommissioned",
        )

    def get_driver_pk(self, obj):
        if obj.kod_driver:
            employee = Employee.objects.filter(number_in_kadry=obj.kod_driver).first()
            if employee:
                return employee.pk
        return None

    def get_has_tag_material(self, obj):
        return has_tag_materials(obj.name)

    def get_car_task_count(self, obj):
        return obj.tasks.filter(is_completed=False).count()


class CarTagSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ("name",)


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
