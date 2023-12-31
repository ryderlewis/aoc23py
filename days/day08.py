from .day import Day


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
        s = 0
        while not all(n[-1] == 'Z' for n in gnodes):
            direction = steps[s % len(steps)]
            gnodes = [nodes[g][0 if direction == 'L' else 1] for g in gnodes]
            s += 1

        return str(s)

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
