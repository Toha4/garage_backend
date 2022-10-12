from collections import Counter

from rest_framework.serializers import ValidationError

from core.models import Employee

from ..models import Work


def find_duplicate(arr):
    return [k for k, v in Counter(arr).items() if v > 1]


def validator_order_works(order_works):
    works_id = []
    for order_work in order_works:
        works_id.append(order_work.get("work").pk)

    duplicate = find_duplicate(works_id)
    if duplicate:
        work = Work.objects.get(pk=duplicate[0])
        raise ValidationError({"error": (f'Работа "{work.name}" повторяется')})


def validator_mechanics_order_work(mechanics, work_id):
    mechanics_id = []
    for mechanic in mechanics:
        mechanics_id.append(mechanic.get("mechanic").pk)

    duplicate = find_duplicate(mechanics_id)
    if duplicate:
        mechanic = Employee.objects.get(pk=duplicate[0])
        work = Work.objects.get(pk=work_id)
        raise ValidationError({"error": (f'Слесарь {mechanic.short_fio} повторяется в работе "{work.name}"')})
