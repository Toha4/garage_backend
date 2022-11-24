from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import QuerySet
from django.db.models import When


def sort_by_types(queryset: QuerySet, types: list) -> QuerySet:
    params = list()
    for index, type_ in enumerate(types, start=1):
        params.append(When(type=type_, then=index))

    queryset = queryset.annotate(sort_type=Case(*params, output_field=IntegerField())).order_by(
        "sort_type",
        "last_name",
    )

    return queryset
