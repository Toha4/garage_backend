from ..models import Entrance


def get_provider_list():
    providers = []

    queryset = (
        Entrance.objects.all().values_list("provider", flat=True).exclude(provider__exact="").distinct().order_by()
    )
    if queryset:
        providers = list(queryset)

    return providers
