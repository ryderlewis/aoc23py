from .day import Day
from collections import namedtuple

Step = namedtuple('Step', 'direction steps rgb')
RGB = namedtuple('RGB', 'red green blue')


class Day18(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        steps = self.parse()
        curr = (0, 0)
        coords = {curr}
        for s in steps:
            mod = (0, 0)
            if s.direction == 'U':
                mod = (-1, 0)
            if s.direction == 'D':
                mod = (1, 0)
            if s.direction == 'L':
                mod = (0, -1)
            if s.direction == 'R':
                mod = (0, 1)

            for _ in range(s.steps):
                curr = (curr[0] + mod[0], curr[1] + mod[1])
                coords.add(curr)

        min_row = min(coord[0] for coord in coords) - 1
        max_row = max(coord[0] for coord in coords) + 1
        min_col = min(coord[1] for coord in coords) - 1
        max_col = max(coord[1] for coord in coords) + 1

        # calculate area by expanding coordinates 1 in each direction, and finding all exterior points
        trench_size = len(coords)
        visited = coords
        to_visit = [(min_row, min_col)]
        while len(to_visit) > 0:
            row, col = to_visit.pop(0)
            if row-1 >= min_row and (row-1, col) not in visited:
                to_visit.append((row-1, col))
                visited.add((row-1, col))
            if row+1 <= max_row and (row+1, col) not in visited:
                to_visit.append((row+1, col))
                visited.add((row+1, col))
            if col-1 >= min_col and (row, col-1) not in visited:
                to_visit.append((row, col-1))
                visited.add((row, col-1))
            if col+1 <= max_col and (row, col+1) not in visited:
                to_visit.append((row, col+1))
                visited.add((row, col+1))

        area = (max_row-min_row+1)*(max_col-min_col+1)-len(visited)+trench_size
        return str(area)

    def part2(self) -> str:
        return "day18 2"

    def parse(self) -> tuple[Step, ...]:
        ret = []
        for line in self.data_lines():
            direction, steps, colors = line.split()
            red, green, blue = map(lambda x: int(x, 16), (colors[2:4], colors[4:6], colors[6:8]))
            ret.append(Step(direction, int(steps), RGB(red, green, blue)))
        return tuple(ret)
