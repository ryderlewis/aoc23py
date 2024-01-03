from .day import Day


class Day17(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid = self._parse()

    def part1(self) -> str:
        return str(self.best_path())

    def part2(self) -> str:
        return "day17 2"

    def best_path(self) -> int:
        start_weight = self._grid[0][0]
        visited = {}
        to_visit = []

        def visit(row, col, direction, curr_steps, curr_weight):
            if curr_steps > 3:
                return
            if row < 0 or row >= len(self._grid):
                return
            if col < 0 or col >= len(self._grid[0]):
                return
            tup = (row, col, direction, curr_steps)
            if tup not in visited or visited[tup] > curr_weight:
                visited[tup] = curr_weight
                to_visit.append((row, col, direction, curr_steps, curr_weight))
        visit(0, 0, 'east', 3, -start_weight)
        visit(0, 0, 'south', 3, -start_weight)

        min_weight = sum(self._grid[r][c] for r in range(len(self._grid)) for c in range(len(self._grid[0])))
        while len(to_visit) > 0:
            row, col, direction, curr_steps, curr_weight = to_visit.pop(0)
            new_weight = curr_weight + self._grid[row][col]
            if row == len(self._grid)-1 and col == len(self._grid[0])-1:
                min_weight = min(new_weight, min_weight)
            if direction == 'east':
                visit(row, col+1, 'east', curr_steps+1, new_weight)
                visit(row-1, col, 'north', 1, new_weight)
                visit(row+1, col, 'south', 1, new_weight)
            elif direction == 'west':
                visit(row, col-1, 'west', curr_steps+1, new_weight)
                visit(row-1, col, 'north', 1, new_weight)
                visit(row+1, col, 'south', 1, new_weight)
            elif direction == 'north':
                visit(row, col+1, 'east', 1, new_weight)
                visit(row, col-1, 'west', 1, new_weight)
                visit(row-1, col, 'north', curr_steps+1, new_weight)
            elif direction == 'south':
                visit(row, col+1, 'east', 1, new_weight)
                visit(row, col-1, 'west', 1, new_weight)
                visit(row+1, col, 'south', curr_steps+1, new_weight)

        return min_weight

    def _parse(self) -> list[list[int]]:
        return [list(map(int, line)) for line in self.data_lines()]
