from django.db.models import Sum

from app.helpers.database import convert_to_localtime
from app.helpers.database import get_period_filter_lookup
from core.models import Car
from orders.constants import COMPLETED
from orders.constants import OTHER
from orders.constants import REPAIR
from orders.constants import TO
from orders.helpers.time_minutes_formated import time_minutes_formated
from orders.models import Order


def get_statistics_car(car_pk, date_begin, date_end):
    car = Car.objects.get(pk=car_pk)

    statistic = []

    if not car_pk:
        return statistic

    queryset = Order.objects.filter(car=car, status=COMPLETED)

    if date_begin and date_end:
        queryset = queryset.filter(get_period_filter_lookup("date_begin", date_begin, date_end))

    # Order count
    order_count = {
        "name_param": "Заказ-нарядов выполненных, шт.",
        "total": queryset.count(),
        "maintenance": queryset.filter(reasons__type=TO).count(),
        "repair": queryset.filter(reasons__type=REPAIR).count(),
        "other": queryset.filter(reasons__type=OTHER).count(),
    }
    statistic.append(order_count)

    # Date last order
    date_last_order = {
        "name_param": "Дата последнего заказ-наряда",
        "total": "",
        "maintenance": __get_data_last_order(queryset, TO),
        "repair": __get_data_last_order(queryset, REPAIR),
        "other": __get_data_last_order(queryset, OTHER),
    }
    statistic.append(date_last_order)

    # Last odometer
    last_odometer = {
        "name_param": "Последние показания одометра",
        "total": "",
        "maintenance": __get_last_odometr(queryset, TO),
        "repair": __get_last_odometr(queryset, REPAIR),
        "other": __get_last_odometr(queryset, OTHER),
    }
    statistic.append(last_odometer)

    # Work_hours
    work_hours = {
        "name_param": "Количество затраченных часов",
        "total": __get_work_hours(queryset, None),
        "maintenance": __get_work_hours(queryset, TO),
        "repair": __get_work_hours(queryset, REPAIR),
        "other": __get_work_hours(queryset, OTHER),
    }
    statistic.append(work_hours)

    # Sum materials
    sum_materials = {
        "name_param": "Затраченная сумма, руб.",
        "total": __get_sum_materials(queryset, None),
        "maintenance": __get_sum_materials(queryset, TO),
        "repair": __get_sum_materials(queryset, REPAIR),
        "other": __get_sum_materials(queryset, OTHER),
    }
    statistic.append(sum_materials)

    return statistic


def __get_data_last_order(queryset, type_reason):
    if type_reason:
        queryset = queryset.filter(reasons__type=type_reason)

    order = queryset.order_by("date_begin").last()
    if order:
        return convert_to_localtime(order.date_begin).strftime("%d.%m.%Y")
    return ""


def __get_last_odometr(queryset, type_reason):
    if type_reason:
        queryset = queryset.filter(reasons__type=type_reason)

    order = queryset.order_by("date_begin").last()
    if order:
        return order.odometer
    return ""


def __get_work_hours(queryset, type_reason):
    if type_reason:
        queryset = queryset.filter(reasons__type=type_reason)

    work_minutes = queryset.aggregate(work_minutes=Sum("order_works__time_minutes"))["work_minutes"]
    if work_minutes:
        return time_minutes_formated(work_minutes)
    return ""


def __get_sum_materials(queryset, type_reason):
    if type_reason:
        queryset = queryset.filter(reasons__type=type_reason)

    sum = queryset.aggregate(sum=Sum("turnovers_from_order__sum"))["sum"]
    if sum:
        return abs(sum)
    return ""
