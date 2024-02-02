from .day import Day
from collections import namedtuple
from functools import cache

Coord = namedtuple('Coord', 'row col')


class Maze:
    def __init__(self, input_lines):
        self.row_count = len(input_lines)
        self.col_count = len(input_lines[0])
        self.grid = tuple(tuple(line) for line in input_lines)
        self._slippery = True

    def max_walk(self) -> int:
        self._slippery = True
        return self._max_walk_recur(frozenset(), Coord(row=0, col=1))

    @cache
    def _max_walk_recur(self, visited: frozenset[tuple[int, int]], coord: Coord) -> int:
        if coord.row == self.row_count - 1 and coord.col == self.col_count - 2:
            return len(visited)

        kind = self.grid[coord.row][coord.col]
        if self._slippery:
            can_left = kind in '.<' and coord.col > 0
            can_right = kind in '.>' and coord.col < self.col_count - 1
            can_up = kind in '.^' and coord.row > 0
            can_down = kind in '.v' and coord.row < self.row_count - 1
        else:
            can_left = coord.col > 0
            can_right = coord.col < self.col_count - 1
            can_up = coord.row > 0
            can_down = coord.row < self.row_count - 1

        next_coords = []
        if can_left:
            next_coords.append(Coord(coord.row, coord.col-1))
        if can_right:
            next_coords.append(Coord(coord.row, coord.col+1))
        if can_up:
            next_coords.append(Coord(coord.row-1, coord.col))
        if can_down:
            next_coords.append(Coord(coord.row+1, coord.col))

        max_len = -1
        v = set(visited)
        v.add(coord)
        for next_coord in next_coords:
            if next_coord not in visited and self.grid[next_coord.row][next_coord.col] in '.<>^v':
                max_len = max(max_len, self._max_walk_recur(frozenset(v), next_coord))
        return max_len

    def max_walk_2(self) -> int:
        self._slippery = False
        return self._max_walk_bfs()

    def _max_walk_bfs(self) -> int:
        """
        Walks through max lengths, starting at both the beginning and end, and meeting in the middle
        """
        start_pos = Coord(row=0, col=1)
        end_pos = Coord(row=self.row_count-1, col=self.col_count-2)
        max_len = 0

        to_visit_start = [(start_pos, {start_pos})]
        to_visit_end = [(end_pos, {end_pos})]

        alt = 0
        while len(to_visit_start) > 0 and len(to_visit_end) > 0:
            if alt == 0:
                to_visit, to_visit_other = to_visit_start, to_visit_end
            else:
                to_visit, to_visit_other = to_visit_end, to_visit_start

            next_to_visit = []
            next_seen = set()
            while len(to_visit) > 0:
                coord, path = to_visit.pop()
                path = frozenset(path)
                if (coord, path) in next_seen:
                    continue
                next_seen.add((coord, path))

                next_coords = []
                if coord.col > 0:
                    next_coords.append(Coord(coord.row, coord.col-1))
                if coord.col < self.col_count - 1:
                    next_coords.append(Coord(coord.row, coord.col+1))
                if coord.row > 0:
                    next_coords.append(Coord(coord.row-1, coord.col))
                if coord.row < self.row_count - 1:
                    next_coords.append(Coord(coord.row+1, coord.col))

                npath = {coord}
                npath.update(path)
                for n in next_coords:
                    if n not in path and self.grid[n.row][n.col] in '.<>^v':
                        for o in to_visit_other:
                            if n == o[0] and npath.isdisjoint(o[1]):
                                max_len = max(max_len, len(npath) + len(o[1]))
                                print(f"So far {max_len}")
                                # if max_len >= 154:
                                #     print(f"path: { {n}|npath|o[1] }")
                                break

                        if not all(n == o[0] or n in o[1] for o in to_visit_other):
                            next_to_visit.append((n, npath))

            if alt == 0:
                to_visit_start = next_to_visit
            else:
                to_visit_end = next_to_visit
            alt += 1
            alt %= 2

        return max_len

    def __str__(self) -> str:
        lines = []
        for row in range(self.row_count):
            line = list('Maze(') if row == 0 else list('     ')
            line.extend(self.grid[row])
            if row == self.row_count - 1:
                line.append(')')
            lines.append(''.join(line))
        return "\n".join(lines)


class Day23(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        maze = Maze(self.data_lines())
        return str(maze.max_walk())

    def part2(self) -> str:
        maze = Maze(self.data_lines())
        return str(maze.max_walk_2())
