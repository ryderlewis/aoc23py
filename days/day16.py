from .day import Day


class Cell:
    def __init__(self, kind):
        self.kind = kind
        self.reset()

    def reset(self):
        self._lit = False
        self._to_west = False
        self._to_north = False
        self._to_east = False
        self._to_south = False

    def _update_dirs(self, dirs):
        self._lit = True
        for d in dirs:
            if d == 'north' and not self._to_north:
                self._to_north = True
                yield 'north'
            if d == 'south' and not self._to_south:
                self._to_south = True
                yield 'south'
            if d == 'east' and not self._to_east:
                self._to_east = True
                yield 'east'
            if d == 'west' and not self._to_west:
                self._to_west = True
                yield 'west'

    @property
    def lit(self) -> bool:
        return self._lit

    def shine_from(self, direction):
        if direction == 'west':
            yield from self.shine_from_west()
        if direction == 'east':
            yield from self.shine_from_east()
        if direction == 'north':
            yield from self.shine_from_north()
        if direction == 'south':
            yield from self.shine_from_south()

    def shine_from_west(self):
        dirs = []
        if self.kind == '/':
            dirs.append('north')
        elif self.kind == '\\':
            dirs.append('south')
        elif self.kind == '|':
            dirs.append('north')
            dirs.append('south')
        else:
            dirs.append('east')
        yield from self._update_dirs(dirs)

    def shine_from_east(self):
        dirs = []
        if self.kind == '/':
            dirs.append('south')
        elif self.kind == '\\':
            dirs.append('north')
        elif self.kind == '|':
            dirs.append('north')
            dirs.append('south')
        else:
            dirs.append('west')
        yield from self._update_dirs(dirs)

    def shine_from_north(self):
        dirs = []
        if self.kind == '/':
            dirs.append('west')
        elif self.kind == '\\':
            dirs.append('east')
        elif self.kind == '-':
            dirs.append('west')
            dirs.append('east')
        else:
            dirs.append('south')
        yield from self._update_dirs(dirs)

    def shine_from_south(self):
        dirs = []
        if self.kind == '/':
            dirs.append('east')
        elif self.kind == '\\':
            dirs.append('west')
        elif self.kind == '-':
            dirs.append('west')
            dirs.append('east')
        else:
            dirs.append('north')
        yield from self._update_dirs(dirs)


class Grid:
    def __init__(self, inputs):
        self._cells = [[Cell(c) for c in line] for line in inputs]
        self._rows = len(self._cells)
        self._cols = len(self._cells[0])

    def reset_cells(self):
        for row in range(self._rows):
            for col in range(self._cols):
                self._cells[row][col].reset()

    def shine(self, start_row, start_col, start_dir_from) -> int:
        self.reset_cells()
        to_visit = [(start_row, start_col, start_dir_from)]
        while len(to_visit) > 0:
            row, col, shine_from_direction = to_visit.pop(0)
            for emit_direction in self._cells[row][col].shine_from(shine_from_direction):
                if emit_direction == 'east' and col+1 < self._cols:
                    to_visit.append((row, col+1, 'west'))
                if emit_direction == 'west' and col-1 >= 0:
                    to_visit.append((row, col-1, 'east'))
                if emit_direction == 'south' and row+1 < self._rows:
                    to_visit.append((row+1, col, 'north'))
                if emit_direction == 'north' and row-1 >= 0:
                    to_visit.append((row-1, col, 'south'))
        return len([1 for r in range(self._rows) for c in range(self._cols) if self._cells[r][c].lit])

    def first_shine(self) -> int:
        return self.shine(0, 0, 'west')

    def max_shine(self) -> int:
        max_shine = 0
        for row in range(self._rows):
            for col in range(self._cols):
                if row == 0:
                    max_shine = max(max_shine, self.shine(row, col, 'north'))
                if row == self._rows-1:
                    max_shine = max(max_shine, self.shine(row, col, 'south'))
                if col == 0:
                    max_shine = max(max_shine, self.shine(row, col, 'west'))
                if col == self._cols-1:
                    max_shine = max(max_shine, self.shine(row, col, 'east'))
        return max_shine


class Day16(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid = Grid(self.data_lines())
        return str(grid.first_shine())

    def part2(self) -> str:
        grid = Grid(self.data_lines())
        return str(grid.max_shine())
