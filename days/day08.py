from .day import Day
from math import lcm


class Day08(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        steps, nodes = self.parse()
        node = 'AAA'
        s = 0
        while node != 'ZZZ':
            direction = steps[s % len(steps)]
            node = nodes[node][0 if direction == 'L' else 1]
            s += 1

        return str(s)

    def part2(self) -> str:
        steps, nodes = self.parse()
        gnodes = [n for n in nodes if n[-1] == 'A']
        counts = []

        for n in gnodes:
            initial, offset = 0, 0
            for s in self.steps(n):
                if initial == 0:
                    initial = s
                elif offset == 0:
                    offset = s - initial
                else:
                    if initial == offset == s - initial - offset:
                        counts.append(initial)
                    else:
                        raise Exception(f"{n}: {initial}, {offset}, {s-initial-offset}")
                    break

        return str(lcm(*counts))

    def steps(self, node):
        steps, nodes = self.parse()
        s = 0
        while True:
            if node[-1] == 'Z':
                yield s
            direction = steps[s % len(steps)]
            node = nodes[node][0 if direction == 'L' else 1]
            s += 1

    def parse(self) -> tuple[str, dict]:
        lines = self.data_lines()
        steps, lines = lines[0], lines[2:]
        nodes = {}
        for line in lines:
            node, _, left, right = line.split()
            left = left[1:-1]
            right = right[:-1]
            nodes[node] = (left, right)
        return steps, nodes
