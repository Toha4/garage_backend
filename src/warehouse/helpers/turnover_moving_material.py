from datetime import datetime

from django.db.transaction import atomic

from ..constants import COMING
from ..constants import EXPENSE
from ..models import Material
from ..models import Turnover
from ..models import Warehouse


@atomic
def turnover_moving_material(data, user):
    material = Material.objects.get(id=data["material"])
    warehouse_outgoing = Warehouse.objects.get(id=data["warehouse_outgoing"])
    warehouse_incoming = Warehouse.objects.get(id=data["warehouse_incoming"])

    date = datetime.strptime(data["date"], "%d.%m.%Y")
    price = data["price"]
    quantity = data["quantity"]
    sum = data["sum"]

    note = f'перемещение из "{warehouse_outgoing.name}" в "{warehouse_incoming.name}"'

    turnover1 = Turnover(
        user=user,
        type=EXPENSE,
        date=date,
        is_correction=True,
        note=note,
        material=material,
        warehouse=warehouse_outgoing,
        price=price,
        quantity=quantity,
        sum=sum,
    )
    turnover2 = Turnover(
        user=user,
        type=COMING,
        date=date,
        is_correction=True,
        note=note,
        material=material,
        warehouse=warehouse_incoming,
        price=price,
        quantity=quantity,
        sum=sum,
    )

    turnover1.save()
    turnover2.save()

    return True
