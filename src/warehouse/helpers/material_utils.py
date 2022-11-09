from datetime import date

from django.db.models import Sum

from app.helpers.postgresql import Round2

from ..constants import COMING
from ..models import Material
from ..models import Turnover


def get_material_in_warehouses(material_pk: str, skip_epmty: bool = False):
    materials_warehouses = []

    queryset = Material.objects.all().filter(pk=material_pk)

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
                        "last_price": get_last_price(material_pk, warehouse["turnovers__warehouse"]),
                    },
                }
            )

    return materials_warehouses


def get_last_price(material_pk: int, warehouse_pk: int | None = None):
    last_price = 0.00

    queryset = Turnover.objects.filter(type=COMING, is_correction=False, material=material_pk)

    if warehouse_pk:
        queryset = queryset.filter(warehouse=warehouse_pk)

    last_turnovers = queryset.order_by("-date", "-pk").first()
    if last_turnovers:
        last_price = last_turnovers.price

    return last_price


def get_average_price(material_pk: int):
    average_price = 0.00

    queryset = (
        Turnover.objects.filter(material=material_pk)
        .values("material")
        .annotate(quantity_sum=Round2(Sum("quantity")), sum_sum=Round2(Sum("sum")))
    )
    if queryset and queryset[0]["quantity_sum"] > 0.0:
        average_price = round(queryset[0]["sum_sum"] / queryset[0]["quantity_sum"], 2)

    return average_price


def get_material_prices(material_pk: int):
    return {
        "last_price": get_last_price(material_pk),
        "average_price": get_average_price(material_pk),
    }


def get_material_remains(material_pk: int, warehouse_pk: int | None = None, date=date.today()):
    remains = 0.00

    queryset = Turnover.objects.filter(material=material_pk, date__lte=date)

    if warehouse_pk:
        queryset = queryset.filter(warehouse=warehouse_pk)

    queryset = queryset.values("material").annotate(quantity_sum=Round2(Sum("quantity")))

    if queryset:
        remains = queryset[0]["quantity_sum"]

    return remains


def has_tag_materials(car_name: str):
    return Material.objects.filter(compatbility__contains=[car_name]).exists()
