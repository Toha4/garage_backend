from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count
from django.db.models import DecimalField
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models.functions import Coalesce

from app.helpers.database import get_period_filter_lookup
from core.models import Car
from orders.constants import COMPLETED


def get_report_cars_queryset(date_begin: str, date_end: str, reason_type: int | None):
    filter_orders = Q(orders__status=COMPLETED) & Q(
        get_period_filter_lookup("orders__date_end", date_begin, date_end, True)
    )

    if reason_type:
        filter_orders = filter_orders & Q(orders__reason__type=reason_type)

    work_minutes_total = Car.objects.annotate(
        work_minutes_total=Sum("orders__order_works__time_minutes", filter=filter_orders)
    ).filter(pk=OuterRef("orders__car"))

    sum_total = Car.objects.annotate(sum_total=Sum("orders__turnovers_from_order__sum", filter=filter_orders)).filter(
        pk=OuterRef("orders__car")
    )

    orders_pk = Car.objects.annotate(orders_pk=ArrayAgg("orders__pk"), filter=filter_orders).filter(
        pk=OuterRef("orders__car")
    )

    queryset = Car.objects.values("pk", "state_number", "name").annotate(
        order_total=Count("orders", filter=filter_orders),
        work_minutes_total=Coalesce(Subquery(work_minutes_total.values("work_minutes_total")), 0),
        sum_total=Coalesce(
            Subquery(sum_total.values("sum_total")), 0.0, output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
        orders_pk=Subquery(orders_pk.values("orders_pk")),
    )

    queryset = queryset.filter(order_total__gt=0)

    return queryset
