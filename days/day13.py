from .day import Day

class Grid:
    def __init__(self, rows):
        self.rows = rows

    def vertical_mirrors(self, smudge_count: int):
        for i in range(1, len(self.rows[0])):
            smudges = 0
            for left, right in zip(range(i-1, -1, -1), range(i, len(self.rows[0]))):
                smudges += len([1 for r in range(len(self.rows)) if self.rows[r][left] != self.rows[r][right]])
                if smudges > smudge_count:
                    break
            if smudges == smudge_count:
                yield i

    def horizontal_mirrors(self, smudge_count: int):
        for i in range(1, len(self.rows)):
            smudges = 0
            for top, bottom in zip(range(i-1, -1, -1), range(i, len(self.rows))):
                smudges += len([1 for c in range(len(self.rows[top])) if self.rows[top][c] != self.rows[bottom][c]])
                if smudges > smudge_count:
                    break
            if smudges == smudge_count:
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
            v = sum(grid.vertical_mirrors(0))
            h = sum(grid.horizontal_mirrors(0))
            # print(f"{grid}: {v} + 100*{h}")
            s += v + 100*h
        return str(s)

    def part2(self) -> str:
        s = 0
        for grid in self.parse():
            v = sum(grid.vertical_mirrors(1))
            h = sum(grid.horizontal_mirrors(1))
            # print(f"{grid}: {v} + 100*{h}")
            s += v + 100*h
        return str(s)

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
