from datetime import date

from django.db.models import Sum

from app.helpers.postgresql import Round2

from ..constants import COMING
from ..models import Material
from ..models import Turnover


def get_material_in_warehouses(material_id: str, skip_epmty: bool = False):
    materials_warehouses = []

    queryset = Material.objects.all().filter(id=material_id)

    queryset = queryset.values("turnovers__warehouse", "turnovers__warehouse__name").annotate(
        quantity=Round2(Sum("turnovers__quantity")), sum=Round2(Sum("turnovers__sum"))
    )

    if skip_epmty:
        queryset = queryset.filter(quantity__gt=0.0)

    queryset = queryset.order_by("name")

    if queryset[0]["turnovers__warehouse"] is not None:
        for warehouse in queryset:
            average_price = round(warehouse["sum"] / warehouse["quantity"], 2) if warehouse["quantity"] > 0 else 0.0
            materials_warehouses.append(
                {
                    "warehouse": warehouse["turnovers__warehouse"],
                    "warehouse_name": warehouse["turnovers__warehouse__name"],
                    "quantity": float(warehouse["quantity"]),
                    "prices": {
                        "average_price": average_price,
                        "last_price": get_last_price(material_id, warehouse["turnovers__warehouse"]),
                    },
                }
            )

    return materials_warehouses


def get_last_price(material_id: int, warehouse_id: int | None = None):
    last_price = 0.00

    queryset = Turnover.objects.filter(type=COMING, is_correction=False, material=material_id)

    if warehouse_id:
        queryset = queryset.filter(warehouse=warehouse_id)

    last_turnovers = queryset.order_by("-date", "-id").first()
    if last_turnovers:
        last_price = last_turnovers.price

    return last_price


def get_average_price(material_id: int):
    average_price = 0.00

    queryset = (
        Turnover.objects.filter(material=material_id)
        .values("material")
        .annotate(quantity_sum=Round2(Sum("quantity")), sum_sum=Round2(Sum("sum")))
    )
    if queryset and queryset[0]["quantity_sum"] > 0.0:
        average_price = round(queryset[0]["sum_sum"] / queryset[0]["quantity_sum"], 2)

    return average_price


def get_material_prices(material_id: int):
    return {
        "last_price": get_last_price(material_id),
        "average_price": get_average_price(material_id),
    }


def get_material_remains(material_id: int, warehouse_id: int | None = None, date=date.today()):
    remains = 0.00

    queryset = Turnover.objects.filter(material=material_id, date__lte=date)

    if warehouse_id:
        queryset = queryset.filter(warehouse=warehouse_id)

    queryset = queryset.values("material").annotate(quantity_sum=Round2(Sum("quantity")))

    if queryset:
        remains = queryset[0]["quantity_sum"]

    return remains
