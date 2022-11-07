from django.db.models import Func


class Round2(Func):
    """Аналог ROUND в SQL"""

    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"
