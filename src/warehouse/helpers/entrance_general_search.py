from django.db.models import Q


def entrance_general_search(queryset, search: str):
    return queryset.filter(
        (
            Q(provider__icontains=search)
            | Q(document_number__icontains=search)
            | Q(turnovers_from_entrance__material__name__icontains=search)
            | Q(note__icontains=search)
        )
    ).distinct()
