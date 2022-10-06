from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Replace


def order_general_search(queryset, search: str):
    return queryset.annotate(
        state_number_without_whitespace=Replace("car__state_number", Value(" "), Value(""))
    ).filter(
        (
            Q(number=search if search.isdigit() else None)
            | Q(car__state_number__icontains=search)
            | Q(state_number_without_whitespace__icontains=search)
            | Q(car__name__icontains=search)
            | Q(reason__name__icontains=search)
            | Q(note__icontains=search)
        )
    )
