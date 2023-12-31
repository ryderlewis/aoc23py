from .day import Day
from collections import namedtuple
from bisect import bisect_left, bisect_right


Race = namedtuple('Race', ['time', 'distance'])

class Day06(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        product = 1
        for r in self.races():
            product *= self.ways(r)
        return str(product)

    def part2(self) -> str:
        r = self.one_race()
        return str(self.ways(r))

    @staticmethod
    def ways(race: Race) -> int:
        # find ways to the left that _don't_ win
        # in this case, l is the "last loser" from the left
        l, r = 0, (race.time+1)//2
        while l < r:
            m = l + (r-l+1)//2
            if m * (race.time - m) <= race.distance:
                l = m
            else:
                r = m-1
        return race.time - l * 2 - 1

    def races(self) -> list[Race]:
        lines = self.data_lines()
        times = map(int, lines.pop(0).split()[1:])
        distances = map(int, lines.pop(0).split()[1:])
        return [Race(time=t, distance=d) for t, d in zip(times, distances)]

    def one_race(self) -> Race:
        lines = self.data_lines()
        t = int(''.join(lines.pop(0).split()[1:]))
        d = int(''.join(lines.pop(0).split()[1:]))
        return Race(time=t, distance=d)
