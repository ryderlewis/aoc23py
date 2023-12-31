from .day import Day
from .day01 import Day01
from .day02 import Day02
from .day03 import Day03
from .day04 import Day04
from .day05 import Day05
from .day06 import Day06
from .day07 import Day07


def factory(*, filename: str, day: int, part: int) -> Day:
    kwargs = {
        'filename': filename,
        'part': part,
    }

    if day == 1:
        return Day01(**kwargs)
    elif day == 2:
        return Day02(**kwargs)
    elif day == 3:
        return Day03(**kwargs)
    elif day == 4:
        return Day04(**kwargs)
    elif day == 5:
        return Day05(**kwargs)
    elif day == 6:
        return Day06(**kwargs)
    elif day == 7:
        return Day07(**kwargs)
    else:
        return Day(**kwargs)
