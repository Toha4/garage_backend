from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .constants import COMING
from .constants import EXPENSE
from .helpers.material_utils import get_material_remains
from .models import Turnover


@receiver(pre_save, sender=Turnover)
def check_before_save(sender, instance, *args, **kwargs):
    if instance.type == COMING and not instance.is_correction and not instance.entrance:
        raise ValidationError({"entrance": ("Отсутсвует поле entrance")})

    if instance.type == EXPENSE and not instance.is_correction and not instance.order:
        raise ValidationError({"entrance": ("Отсутсвует поле order")})

    if instance.order and instance.entrance:
        raise ValidationError({"entrance": ("Должно быть одно из полей 'entrance' или 'order'")})

    if instance.is_correction and (instance.order or instance.entrance):
        raise ValidationError({"is_correction": ("Поля 'entrance' и 'order' не должны указываться при корректировке")})

    if instance.is_correction is True and len(instance.note) <= 0:
        raise ValidationError({"is_correction": ("Поле 'note' обязательно при корректировки")})

    quantity = float(abs(instance.quantity))
    price = float(instance.price)
    sum_ = float(abs(instance.sum))

    if round(quantity * price, 2) != sum_:
        raise ValidationError({"sum": ("Неверная сумма")})

    if quantity <= 0.00:
        raise ValidationError({"quantity": ("Количество должно быть больше 0")})

    if price <= 0.00:
        raise ValidationError({"price": ("Цена должно быть больше 0")})

    if sum_ <= 0.00:
        raise ValidationError({"sum": ("Сумма должно быть больше 0")})

    if instance.type == EXPENSE and quantity > get_material_remains(
        instance.material, instance.warehouse, instance.date
    ):
        raise ValidationError({"quantity": ("Вы пытаетесь списать больше чем в наличии на складе")})
