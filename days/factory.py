from .day import Day
from .day01 import Day01


def factory(*, filename: str, day: int, part: int) -> Day:
    kwargs = {
        'filename': filename,
        'part': part,
    }

    if day == 1:
        return Day01(**kwargs)
    else:
        return Day(**kwargs)
