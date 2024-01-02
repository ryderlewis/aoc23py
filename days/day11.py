from .day import Day


class Day11(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rows = 0
        self._cols = 0

    def part1(self) -> str:
        grid = self.grid()
        galaxies = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']
        s = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                s += abs(galaxies[i][0] - galaxies[j][0])
                s += abs(galaxies[i][1] - galaxies[j][1])
        return str(s)

    def part2(self) -> str:
        return "dayXX 2"

    def grid(self) -> list[list[str]]:
        inputs = self.data_lines()
        outputs = []
        blank_rows = set([r for r, line in enumerate(inputs) if not any(c == '#' for c in line)])
        blank_cols = set([c for c in range(len(inputs[0])) if not any(line[c] == '#' for line in inputs)])
        for row, line in enumerate(inputs):
            if row in blank_rows:
                for double in range(2):
                    outputs.append(['.' for _ in range(len(inputs[0]) + len(blank_cols))])
            else:
                output = []
                for col, char in enumerate(line):
                    if col in blank_cols:
                        for double in range(2):
                            output.append('.')
                    else:
                        output.append(char)
                outputs.append(output)
        return outputs

