from datetime import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import DecimalField
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models.functions import Coalesce

from app.helpers.database import get_period_filter_lookup
from app.helpers.postgresql import Round2
from warehouse.constants import EXPENSE
from warehouse.models import Material


def get_report_materials_queryset(date_begin: str, date_end: str):
    remains_quantity = Material.objects.annotate(
        remains_quantity=Round2(
            Sum(
                "turnovers__quantity",
                filter=Q(turnovers__date__lte=datetime.strptime(date_end, "%d.%m.%Y"))
                & Q(turnovers__warehouse=OuterRef("turnovers__warehouse")),
            )
        )
    ).filter(pk=OuterRef("pk"))

    filter_turnovers = (
        Q(turnovers__type=EXPENSE)
        & Q(turnovers__is_correction=False)
        & get_period_filter_lookup("turnovers__order__date_end", date_begin, date_end)
    )

    queryset = Material.objects.values(
        "pk", "name", "unit__name", "unit__is_precision_point", "turnovers__warehouse", "turnovers__warehouse__name"
    ).annotate(
        used_quantity=Coalesce(
            Sum("turnovers__quantity", filter=filter_turnovers),
            0.0,
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        used_sum=Coalesce(
            Sum("turnovers__sum", filter=filter_turnovers),
            0.0,
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        remains_quantity=Subquery(remains_quantity.values("remains_quantity")),
        turnovers_pk=ArrayAgg("turnovers__pk", filter=filter_turnovers),
    )

    queryset = queryset.filter(used_quantity__lt=0.0)

    return queryset
