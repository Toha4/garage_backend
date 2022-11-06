from django.db.models import Q
from django.db.models import Sum

from app.helpers.postgresql import Round2

from ..models import Material


def get_queryset_materials_remains(
    category: str,
    warehouse: str,
    compatbility: str,
    hide_empty: str,
    search_name: str,
    group_warehouse: bool,
):
    queryset = Material.objects.all()

    if category:
        queryset = queryset.filter(category=category)

    if compatbility and group_warehouse:
        queryset = queryset.filter(
            Q(compatbility__overlap=[car_tag for car_tag in compatbility.split(",")]) | Q(compatbility__len=0)
        )
    elif compatbility:
        queryset = queryset.filter(compatbility__overlap=[car_tag for car_tag in compatbility.split(",")])

    if search_name:
        queryset = queryset.filter(name__icontains=search_name)

    quantity_annotate = Sum("turnovers__quantity")
    sum_annotate = Sum("turnovers__sum")
    values = ["id", "name", "category", "category__name", "unit__name", "unit__is_precision_point", "compatbility"]

    if warehouse:
        quantity_annotate = Sum("turnovers__quantity", filter=Q(turnovers__warehouse=warehouse))
        sum_annotate = Sum("turnovers__sum", filter=Q(turnovers__warehouse=warehouse))

    if group_warehouse:
        values.extend(["turnovers__warehouse", "turnovers__warehouse__name"])

    queryset = (
        queryset.values(*values)
        .annotate(quantity=Round2(quantity_annotate), sum=Round2(sum_annotate))
        .order_by("name")
    )

    if hide_empty == "true" or warehouse:
        queryset = queryset.exclude(Q(quantity__lte=0.0) | Q(quantity__isnull=True))

    return queryset
