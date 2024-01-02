from .day import Day


class Day11(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rows = 0
        self._cols = 0

    def part1(self) -> str:
        return self.result(expand=1)

    def part2(self) -> str:
        return self.result(expand=999_999)

    def result(self, *, expand: int) -> str:
        galaxies = self.galaxy_coords(expand=expand)
        s = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                s += abs(galaxies[i][0] - galaxies[j][0])
                s += abs(galaxies[i][1] - galaxies[j][1])
        return str(s)

    def galaxy_coords(self, *, expand: int) -> list[tuple[int, int]]:
        inputs = self.data_lines()
        coords = []
        blank_rows = set([r for r, line in enumerate(inputs) if not any(c == '#' for c in line)])
        blank_cols = set([c for c in range(len(inputs[0])) if not any(line[c] == '#' for line in inputs)])

        row_expand = 0
        for row, line in enumerate(inputs):
            if row in blank_rows:
                row_expand += expand
            else:
                col_expand = 0
                for col, char in enumerate(line):
                    if col in blank_cols:
                        col_expand += expand
                    elif char == '#':
                        coords.append((row + row_expand, col + col_expand))
        return coords
