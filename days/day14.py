from .day import Day


class Grid:
    def __init__(self, inputs):
        self._grid = [list(line) for line in inputs]

    def __str__(self) -> str:
        output = []
        for i, line in enumerate(self._grid):
            starting = 'Grid(' if i == 0 else '     '
            ending = ')' if i == len(self._grid) - 1 else ''
            output.append(f"{starting}{line}{ending}")
        return "\n".join(output)

    def load(self) -> int:
        load = 0
        for row in range(len(self._grid)):
            weight = len(self._grid)-row
            load += weight * len([c for c in self._grid[row] if c == 'O'])
        return load

    def north(self) -> None:
        for row in range(len(self._grid)):
            for col in range(len(self._grid[0])):
                if self._grid[row][col] == '.':
                    curr_row = row
                    for iter_row in range(row+1, len(self._grid)):
                        if self._grid[iter_row][col] == 'O':
                            self._grid[iter_row][col] = '.'
                            self._grid[curr_row][col] = 'O'
                            curr_row += 1
                        elif self._grid[iter_row][col] == '#':
                            break


class Day14(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid = Grid(self.data_lines())
        grid.north()
        return str(grid.load())

    def part2(self) -> str:
        grid = Grid(self.data_lines())
        return str(grid)
