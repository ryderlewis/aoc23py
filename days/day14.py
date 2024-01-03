from .day import Day


class Grid:
    def __init__(self, inputs):
        self._grid = [list(line) for line in inputs]

    def __str__(self) -> str:
        output = []
        for i, line in enumerate(self._grid):
            starting = 'Grid(' if i == 0 else '     '
            ending = ')' if i == len(self._grid) - 1 else ''
            output.append(f"{starting}{''.join(line)}{ending}")
        return "\n".join(output)

    def load(self) -> int:
        load = 0
        for row in range(len(self._grid)):
            weight = len(self._grid)-row
            load += weight * len([c for c in self._grid[row] if c == 'O'])
        return load

    def spin(self) -> None:
        self.north()
        self.west()
        self.south()
        self.east()

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

    def south(self) -> None:
        for row in range(len(self._grid)-1, -1, -1):
            for col in range(len(self._grid[0])):
                if self._grid[row][col] == '.':
                    curr_row = row
                    for iter_row in range(row-1, -1, -1):
                        if self._grid[iter_row][col] == 'O':
                            self._grid[iter_row][col] = '.'
                            self._grid[curr_row][col] = 'O'
                            curr_row -= 1
                        elif self._grid[iter_row][col] == '#':
                            break

    def west(self) -> None:
        for col in range(len(self._grid[0])):
            for row in range(len(self._grid)):
                if self._grid[row][col] == '.':
                    curr_col = col
                    for iter_col in range(col+1, len(self._grid[0])):
                        if self._grid[row][iter_col] == 'O':
                            self._grid[row][iter_col] = '.'
                            self._grid[row][curr_col] = 'O'
                            curr_col += 1
                        elif self._grid[row][iter_col] == '#':
                            break

    def east(self) -> None:
        for col in range(len(self._grid[0])-1, -1, -1):
            for row in range(len(self._grid)):
                if self._grid[row][col] == '.':
                    curr_col = col
                    for iter_col in range(col-1, -1, -1):
                        if self._grid[row][iter_col] == 'O':
                            self._grid[row][iter_col] = '.'
                            self._grid[row][curr_col] = 'O'
                            curr_col -= 1
                        elif self._grid[row][iter_col] == '#':
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
        memo = {}
        for i in range(1000):
            gstr = str(grid)
            if gstr in memo:
                # print(f"cycle {i} first seen at {memo[gstr]}")
                # how many more spins necessary?
                remaining = (1_000_000_000 - memo[gstr]) % (i - memo[gstr])
                # print(f"remaining: {remaining}")
                for _ in range(remaining):
                    grid.spin()
                break
            else:
                memo[gstr] = i
            grid.spin()
        return str(grid.load())
