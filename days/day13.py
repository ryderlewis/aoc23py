from .day import Day

class Grid:
    def __init__(self, rows):
        self.rows = rows

    def vertical_mirrors(self):
        for i in range(1, len(self.rows[0])):
            all_good = True
            for left, right in zip(range(i-1, -1, -1), range(i, len(self.rows[0]))):
                if any(self.rows[r][left] != self.rows[r][right] for r in range(len(self.rows))):
                    all_good = False
                    break
            if all_good:
                yield i

    def horizontal_mirrors(self):
        for i in range(1, len(self.rows)):
            all_good = True
            for top, bottom in zip(range(i-1, -1, -1), range(i, len(self.rows))):
                if self.rows[top] != self.rows[bottom]:
                    all_good = False
                    break
            if all_good:
                yield i

    def __str__(self) -> str:
        output = []
        for i, line in enumerate(self.rows):
            starting = 'Grid(' if i == 0 else '     '
            ending = ')' if i == len(self.rows) - 1 else ''
            output.append(f"{starting}{line}{ending}")
        return "\n".join(output)


class Day13(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = 0
        for grid in self.parse():
            v = sum(grid.vertical_mirrors())
            h = sum(grid.horizontal_mirrors())
            # print(f"{grid}: {v} + 100*{h}")
            s += v + 100*h
        return str(s)

    def part2(self) -> str:
        return "dayXX 2"

    def parse(self) -> tuple[Grid, ...]:
        grids = []
        cur_grid = []
        for line in self.data_lines():
            if line == '':
                grids.append(Grid(cur_grid))
                cur_grid = []
            else:
                cur_grid.append(line)
        grids.append(Grid(cur_grid))
        return tuple(grids)
