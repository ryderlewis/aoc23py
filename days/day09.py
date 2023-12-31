from .day import Day


class Day09(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        sequences = self.parse()
        return str(sum(self.next_value(s) for s in sequences))

    def part2(self) -> str:
        sequences = self.parse()
        return str(sum(self.prev_value(s) for s in sequences))

    @staticmethod
    def next_value(sequence) -> int:
        stack = [sequence]
        while not all(x == 0 for x in stack[-1]):
            stack.append(tuple(stack[-1][i]-stack[-1][i-1] for i in range(1, len(stack[-1]))))
        return sum(s[-1] for s in stack)

    @staticmethod
    def prev_value(sequence) -> int:
        stack = [sequence]
        while not all(x == 0 for x in stack[-1]):
            stack.append(tuple(stack[-1][i]-stack[-1][i-1] for i in range(1, len(stack[-1]))))
        val = stack.pop()[0]
        while len(stack) > 0:
            left = stack.pop()[0]
            val = left - val
        return val

    def parse(self) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(map(int, line.split())) for line in self.data_lines())
