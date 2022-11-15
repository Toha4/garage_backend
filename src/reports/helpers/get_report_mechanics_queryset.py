from datetime import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import CharField
from django.db.models import Count
from django.db.models import F
from django.db.models import Func
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models import Value as V
from django.db.models.functions import Cast
from django.db.models.functions import Coalesce
from django.db.models.functions import Concat

from app.helpers.database import get_period_filter_lookup
from core.constants import MECHANIC
from core.models import Employee
from orders.constants import COMPLETED
from orders.models import OrderWorkMechanic


def get_report_mechanics_queryset(date_begin: str, date_end: str):
    filter_orders = Q(order_works__order_work__order__status=COMPLETED) & Q(
        get_period_filter_lookup("order_works__order_work__order__date_end", date_begin, date_end)
    )

    work_minutes_total = Employee.objects.annotate(
        work_minutes_total=Sum(
            Coalesce("order_works__time_minutes", "order_works__order_work__time_minutes", 0), filter=filter_orders
        )
    ).filter(pk=OuterRef("pk"))

    unique_repaired_cars_total = Employee.objects.annotate(
        unique_repaired_cars_total=Count("order_works__order_work__order__car", distinct=True, filter=filter_orders)
    ).filter(pk=OuterRef("pk"))

    orders_pk = Employee.objects.annotate(
        orders_pk=ArrayAgg("order_works__order_work__order__pk", distinct=True, filter=filter_orders)
    ).filter(pk=OuterRef("pk"))

    formated_note_date = Func(F("notes__date"), V("dd.MM.yyyy"), function="to_char", output_field=CharField())
    note_list = Employee.objects.annotate(
        note_list=ArrayAgg(
            Concat(
                formated_note_date,
                V(" - "),
                Cast("notes__note", CharField()),
                output_filed=CharField(),
            ),
            distinct=True,
            filter=get_period_filter_lookup("notes__date", date_begin, date_end),
        )
    ).filter(pk=OuterRef("pk"))

    queryset = (
        Employee.objects.filter(type=MECHANIC)
        .filter(Q(date_dismissal__isnull=True) | Q(date_dismissal__gte=datetime.strptime(date_begin, "%d.%m.%Y")))
        .values("pk", "first_name", "last_name", "patronymic")
        .annotate(
            work_minutes_total=Coalesce(Subquery(work_minutes_total.values("work_minutes_total")), 0),
            repaired_cars_total=Coalesce(Subquery(unique_repaired_cars_total.values("unique_repaired_cars_total")), 0),
            orders_pk=Subquery(orders_pk.values("orders_pk")),
            note_list=Subquery(note_list.values("note_list")),
        )
    )

    return queryset


def get_works_mechanics_queryset(mechanik_pk: int, orders_pk: list):
    queryset = (
        OrderWorkMechanic.objects.values(
            "order_work__order__pk",
            "order_work__order__number",
            "order_work__work__name",
            "order_work__quantity",
        )
        .annotate(time_minutes=Coalesce("time_minutes", "order_work__time_minutes", 0))
        .filter(mechanic=mechanik_pk, order_work__order__pk__in=orders_pk)
    )

    return queryset
