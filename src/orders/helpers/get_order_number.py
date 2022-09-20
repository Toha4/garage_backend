def get_order_number() -> int:
    from ..models import Order

    last_order = Order.objects.order_by("-number").first()
    if last_order:
        return last_order.number + 1
    return 1
