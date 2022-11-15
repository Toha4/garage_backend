import math


def time_minutes_formated(tyme_minutes: int) -> str:
    time_str = ""

    if not tyme_minutes:
        return time_str

    minutes = math.floor(tyme_minutes % 60)
    hours = math.floor((tyme_minutes / 60))

    if hours:
        time_str += f"{hours}ч "

    if minutes:
        time_str += f"{minutes}м"

    return time_str
