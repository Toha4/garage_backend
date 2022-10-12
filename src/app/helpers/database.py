from datetime import datetime

from django.db.models import Q
from django.utils import timezone

import pytz


def get_period_filter_lookup(field_name, date_begin, date_end, is_filed_datetime=False):
    argument_type = ""
    if is_filed_datetime:
        argument_type = "__date"

    lookup = Q()
    if date_begin is not None and date_end is not None:
        lookup = Q(
            **{
                f"{field_name}{argument_type}__range": (
                    datetime.strptime(date_begin, "%d.%m.%Y"),
                    datetime.strptime(date_end, "%d.%m.%Y"),
                )
            },
        )
    elif date_begin is not None:
        lookup = Q(**{f"{field_name}{argument_type}__gte": datetime.strptime(date_begin, "%d.%m.%Y")})
    elif date_end is not None:
        lookup = Q(**{f"{field_name}{argument_type}__lte": datetime.strptime(date_end, "%d.%m.%Y")})

    return lookup


def convert_to_localtime(utctime):
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz
