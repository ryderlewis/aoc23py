from .day import Day
from collections import namedtuple

Step = namedtuple('Step', 'direction steps')
Coordinate = namedtuple('Coordinate', 'x y')


class Day18(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def area(steps: tuple[Step, ...]) -> int:
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
        return area

    def part1(self) -> str:
        s = []
        for line in self.data_lines():
            direction, steps, _ = line.split()
            s.append(Step(direction, int(steps)))
        return str(self.area(tuple(s)))

    def part2(self) -> str:
        coords = self.coordinates()

        s = 0
        p = 0
        for i in range(len(coords)):
            c1, c2 = coords[i], coords[(i+1) % len(coords)]
            s += (c1.x * c2.y - c2.x * c1.y)
            p += abs(c1.x - c2.x) + abs(c1.y - c2.y)
        polygon_area = abs(s)/2
        outside_area = 0.5 * p + 1

        return str(int(polygon_area + outside_area))

    def coordinates(self) -> tuple[Coordinate, ...]:
        ret = []
        x, y = 0, 0
        for line in self.data_lines():
            _, _, rgb = line.split()
            steps = int(rgb[2:7], 16)
            di = int(rgb[7:8])
            if di == 0:  # R
                x += steps
            elif di == 1:  # D
                y -= steps
            elif di == 2:  # L
                x -= steps
            else:  # U
                y += steps
            ret.append(Coordinate(x=x, y=y))
        return tuple(ret[-1:] + ret[:-1])
