from .day import Day
from re import finditer


class Day01(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = 0
        for d in self.data_lines():
            n = []
            for c in d:
                if '0' <= c <= '9':
                    n.append(int(c))
            s += 10 * n[0] + n[-1]
        return str(s)

    def part2(self) -> str:
        s = 0
        vals = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
        }
        for d in self.data_lines():
            n = []
            for v in finditer(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", d):
                if v[1] in vals:
                    n.append(vals[v[1]])
                else:
                    n.append(int(v[1]))
            s += 10 * n[0] + n[-1]
        return str(s)
