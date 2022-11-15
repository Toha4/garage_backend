from django.conf import settings

from rest_framework.serializers import DateField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from core.models import Car
from core.models import Employee
from orders.models import Order
from orders.models import OrderWork
from orders.models import OrderWorkMechanic
from warehouse.models import Turnover

from ..helpers.get_report_mechanics_queryset import get_works_mechanics_queryset
from ..models import EmployeeNote


class EmployeeNoteSerializer(ModelSerializer):
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)
    employee_short_fio = SerializerMethodField()

    class Meta:
        model = EmployeeNote
        fields = (
            "pk",
            "employee",
            "employee_short_fio",
            "date",
            "note",
        )

    def get_employee_short_fio(self, obj):
        return obj.employee.short_fio


class ReportOrderShortSerializer(ModelSerializer):
    date_begin = DateTimeField(**settings.SERIALIZER_DATE_PARAMS)

    class Meta:
        model = Order
        fields = (
            "pk",
            "number",
            "date_begin",
            "note",
        )


class ReportOrderWorksShortSerializer(ModelSerializer):
    order_pk = SerializerMethodField()
    order_number = SerializerMethodField()
    work_name = SerializerMethodField()

    class Meta:
        model = OrderWork
        fields = (
            "order_pk",
            "order_number",
            "work_name",
            "quantity",
            "time_minutes",
        )

    def get_order_pk(self, obj):
        return obj.order.pk

    def get_order_number(self, obj):
        return obj.order.number

    def get_work_name(self, obj):
        return obj.work.name


class ReportTurnoverShortSerializer(ModelSerializer):
    order_pk = SerializerMethodField()
    order_number = SerializerMethodField()
    warehouse_pk = SerializerMethodField()
    material_name = SerializerMethodField()
    material_unit_name = SerializerMethodField()
    material_unit_is_precision_point = SerializerMethodField()
    quantity = SerializerMethodField()
    sum = SerializerMethodField()

    class Meta:
        model = Turnover
        fields = (
            "order_pk",
            "order_number",
            "warehouse_pk",
            "material_name",
            "material_unit_name",
            "material_unit_is_precision_point",
            "quantity",
            "sum",
        )

    def get_order_pk(self, obj):
        return obj.order.pk

    def get_order_number(self, obj):
        return obj.order.number

    def get_warehouse_pk(self, obj):
        return obj.warehouse.pk

    def get_material_name(self, obj):
        return obj.material.name

    def get_material_unit_name(self, obj):
        return obj.material.unit.name

    def get_material_unit_is_precision_point(self, obj):
        return obj.material.unit.is_precision_point

    def get_quantity(self, obj):
        return abs(obj.quantity)

    def get_sum(self, obj):
        return abs(obj.sum)


class ReportCarSerializer(ModelSerializer):
    order_total = SerializerMethodField()
    work_minutes_total = SerializerMethodField()
    sum_total = SerializerMethodField()
    orders = SerializerMethodField()
    works = SerializerMethodField()
    materials = SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "pk",
            "state_number",
            "name",
            "order_total",
            "work_minutes_total",
            "sum_total",
            "orders",
            "works",
            "materials",
        )

    def get_order_total(self, obj):
        return obj.get("order_total", 0)

    def get_work_minutes_total(self, obj):
        return obj.get("work_minutes_total", 0)

    def get_sum_total(self, obj):
        return abs(obj.get("sum_total", 0.0))

    def get_orders(self, obj):
        orders_pk = obj.get("orders_pk")
        if orders_pk:
            queryset = Order.objects.filter(pk__in=orders_pk).order_by("number")
            return ReportOrderShortSerializer(queryset, many=True).data
        return []

    def get_works(self, obj):
        orders_pk = obj.get("orders_pk")
        if orders_pk:
            queryset = OrderWork.objects.filter(order__pk__in=orders_pk).order_by("order__number")
            return ReportOrderWorksShortSerializer(queryset, many=True).data
        return []

    def get_materials(self, obj):
        orders_pk = obj.get("orders_pk")
        if orders_pk:
            queryset = Turnover.objects.filter(order__pk__in=orders_pk).order_by("order__number")
            return ReportTurnoverShortSerializer(queryset, many=True).data
        return []


class ReportWorksMechanicSerializer(ModelSerializer):
    order_pk = SerializerMethodField()
    order_number = SerializerMethodField()
    work_name = SerializerMethodField()
    quantity = SerializerMethodField()
    time_minutes = SerializerMethodField()

    class Meta:
        model = OrderWorkMechanic
        fields = (
            "order_pk",
            "order_number",
            "work_name",
            "quantity",
            "time_minutes",
        )

    def get_order_pk(self, obj):
        return obj.get("order_work__order__pk")

    def get_order_number(self, obj):
        return obj.get("order_work__order__number")

    def get_work_name(self, obj):
        return obj.get("order_work__work__name")

    def get_quantity(self, obj):
        return obj.get("order_work__quantity")

    def get_time_minutes(self, obj):
        return obj.get("time_minutes")


class ReportMechanicsSerializer(ModelSerializer):
    short_fio = SerializerMethodField()
    work_minutes_total = SerializerMethodField()
    repaired_cars_total = SerializerMethodField()
    note_list = SerializerMethodField()
    works = SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "pk",
            "short_fio",
            "work_minutes_total",
            "repaired_cars_total",
            "note_list",
            "works",
        )

    def get_short_fio(self, obj):
        last_name = obj.get("last_name")
        first_name = obj.get("first_name")
        patronymic = obj.get("patronymic")

        return f"{last_name} {first_name[0]}. {patronymic[0]}."

    def get_work_minutes_total(self, obj):
        return obj.get("work_minutes_total", 0)

    def get_repaired_cars_total(self, obj):
        return obj.get("repaired_cars_total", 0)

    def get_note_list(self, obj):
        note_list = obj.get("note_list")
        if note_list:
            return note_list
        return []

    def get_works(self, obj):
        pk = obj.get("pk")
        orders_pk = obj.get("orders_pk")
        if pk and orders_pk:
            queryset = get_works_mechanics_queryset(pk, orders_pk)
            return ReportWorksMechanicSerializer(queryset, many=True).data
        return []


class ReportMaterialSerializer(ModelSerializer):
    warehouse = SerializerMethodField()
    warehouse_name = SerializerMethodField()
    material_unit_name = SerializerMethodField()
    material_unit_is_precision_point = SerializerMethodField()
    used_quantity = SerializerMethodField()
    used_sum = SerializerMethodField()
    remains_quantity = SerializerMethodField()
    turnovers = SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "pk",
            "warehouse",
            "warehouse_name",
            "name",
            "material_unit_name",
            "material_unit_is_precision_point",
            "used_quantity",
            "used_sum",
            "remains_quantity",
            "turnovers",
        )

    def get_warehouse(self, obj):
        return obj.get("turnovers__warehouse")

    def get_warehouse_name(self, obj):
        return obj.get("turnovers__warehouse__name")

    def get_material_unit_name(self, obj):
        return obj.get("unit__name")

    def get_material_unit_is_precision_point(self, obj):
        return obj.get("unit__is_precision_point")

    def get_used_quantity(self, obj):
        return abs(obj.get("used_quantity"))

    def get_used_sum(self, obj):
        return abs(obj.get("used_sum"))

    def get_remains_quantity(self, obj):
        return obj.get("remains_quantity")

    def get_turnovers(self, obj):
        turnovers_pk = obj.get("turnovers_pk")
        if turnovers_pk:
            queryset = Turnover.objects.filter(pk__in=turnovers_pk).order_by("order__number")
            return ReportTurnoverShortSerializer(queryset, many=True).data
        return []
