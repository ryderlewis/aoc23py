from .day import Day


class Board:
    def __init__(self):
        self._numbers = []
        self._symbols = []

    def add_number(self, row, col, val):
        self._numbers.append((row, col, val))

    def add_symbol(self, row, col, val):
        self._symbols.append((row, col, val))

    def sym_nums(self):
        for r, c, v in self._numbers:
            if any(r - 1 <= sr <= r + 1 and c - 1 <= sc <= c + len(v) for sr, sc, _ in self._symbols):
                yield r, c, v

class Day03(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        b = self.board()
        s = 0
        for r, c, v in b.sym_nums():
            s += int(v)
        return str(s)

    def part2(self) -> str:
        return "day03 2"

    def board(self) -> Board:
        b = Board()
        for row, line in enumerate(self.data_lines()):
            start_col = None
            for col, char in enumerate(line):
                if char == '.':
                    if start_col is not None:
                        b.add_number(row, start_col, line[start_col:col])
                        start_col = None
                elif '0' <= char <= '9':
                    if start_col is None:
                        start_col = col
                else:
                    if start_col is not None:
                        b.add_number(row, start_col, line[start_col:col])
                        start_col = None
                    b.add_symbol(row, col, str(char))
            if start_col is not None:
                b.add_number(row, start_col, line[start_col:])

        return b
