from datetime import datetime

from .day import Day
from collections import namedtuple
from functools import cache

Coord = namedtuple('Coord', 'row col')


class Maze:
    def __init__(self, input_lines):
        self.row_count = len(input_lines)
        self.col_count = len(input_lines[0])
        self.grid = tuple(tuple(line) for line in input_lines)

    def max_walk(self) -> int:
        return self._max_walk_slippery(frozenset(), Coord(row=0, col=1))

    @cache
    def _max_walk_slippery(self, visited: frozenset[tuple[int, int]], coord: Coord) -> int:
        if coord.row == self.row_count - 1 and coord.col == self.col_count - 2:
            return len(visited)

        kind = self.grid[coord.row][coord.col]
        can_left = kind in '.<' and coord.col > 0
        can_right = kind in '.>' and coord.col < self.col_count - 1
        can_up = kind in '.^' and coord.row > 0
        can_down = kind in '.v' and coord.row < self.row_count - 1

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
                max_len = max(max_len, self._max_walk_slippery(frozenset(v), next_coord))
        return max_len

    def max_walk_2(self) -> int:
        return self._max_walk_pruning()

    def _max_walk_bfs(self) -> int:
        """
        Walks through max lengths, starting at both the beginning and end, and meeting in the middle
        """
        start_pos = Coord(row=0, col=1)
        end_pos = Coord(row=self.row_count-1, col=self.col_count-2)
        max_len = 0

        to_visit_start = [(start_pos, {start_pos})]
        to_visit_end = [(end_pos, {end_pos})]

        alt = False
        loop_count = 0
        while len(to_visit_start) > 0 and len(to_visit_end) > 0:
            loop_count += 1
            alt = not alt
            if alt:
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
                    # move left. but if we're on the top or bottom row, we can't do this
                    if 0 < coord.row < self.row_count - 1:
                        next_coords.append(Coord(coord.row, coord.col-1))
                if coord.col < self.col_count - 1:
                    # move right
                    next_coords.append(Coord(coord.row, coord.col+1))
                if coord.row > 0:
                    # move up. but if we're on the left or right column, we can't do this
                    if 0 < coord.col < self.col_count - 1:
                        next_coords.append(Coord(coord.row-1, coord.col))
                if coord.row < self.row_count - 1:
                    # move down
                    next_coords.append(Coord(coord.row+1, coord.col))

                npath = {coord}
                npath.update(path)
                for n in next_coords:
                    if n not in path and self.grid[n.row][n.col] in '.<>^v':
                        for o in to_visit_other:
                            if n == o[0] and npath.isdisjoint(o[1]):
                                new_max_len = max(max_len, len(npath) + len(o[1]))
                                if new_max_len > max_len:
                                    max_len = new_max_len
                                    print(f"{datetime.now()}: So far {max_len}")
                                break

                        if not all(n == o[0] or n in o[1] for o in to_visit_other):
                            next_to_visit.append((n, npath))

            if alt:
                to_visit_start = next_to_visit
            else:
                to_visit_end = next_to_visit

        print(f"{loop_count=}")
        return max_len

    def _max_walk_pruning(self) -> int:
        """
        Walks through finding the max length, and any time there's a branch to take,
        verifies that the branch has a path to the target
        """
        start_pos = Coord(row=0, col=1)
        end_pos = Coord(row=self.row_count-1, col=self.col_count-2)
        max_len = 0

        to_visit = [(start_pos, frozenset({start_pos}))]

        loop_count = 0
        # next_seen = set()

        while len(to_visit) > 0:
            loop_count += 1
            coord, path = to_visit.pop()
            # if (coord, path) in next_seen:
            #     continue
            # next_seen.add((coord, path))

            potential_next_coords = []
            if coord.col > 0:
                # move left. but if we're on the top or bottom row, we can't do this
                if 0 < coord.row < self.row_count - 1:
                    potential_next_coords.append(Coord(coord.row, coord.col-1))
            if coord.col < self.col_count - 1:
                # move right
                potential_next_coords.append(Coord(coord.row, coord.col+1))
            if coord.row > 0:
                # move up. but if we're on the left or right column, we can't do this
                if 0 < coord.col < self.col_count - 1:
                    potential_next_coords.append(Coord(coord.row-1, coord.col))
            if coord.row < self.row_count - 1:
                # move down
                potential_next_coords.append(Coord(coord.row+1, coord.col))

            next_coords = [c for c in potential_next_coords
                           if c not in path
                           and self.grid[c.row][c.col] in '.<>^v']

            if not next_coords:
                continue

            npath = {coord}
            npath.update(path)
            npath = frozenset(npath)

            if len(next_coords) > 1:
                n = self._prune_next_coords(coord, end_pos, npath, next_coords)
                if len(n) < len(next_coords):
                    print(f"{loop_count=}, pruned {len(next_coords)} down to {len(n)} next paths, {max_len=}, {len(to_visit)=}")
                    next_coords = n

            for n in next_coords:
                if n == end_pos:
                    new_max_len = max(max_len, len(npath))
                    if new_max_len > max_len:
                        max_len = new_max_len
                        print(f"{datetime.now()}: So far {max_len}, len(to_visit)={len(to_visit)}")
                else:
                    to_visit.append((n, npath))

        print(f"{loop_count=}")
        return max_len

    def _prune_next_coords(self, coord, end_pos, cpath, next_coords):
        ret = []
        # see if there's a path from coord to end_pos. for each one, do a BFS to see if we get to end_pos
        for nc in next_coords:
            to_visit = [(nc, cpath)]
            while len(to_visit) > 0:
                coord, path = to_visit.pop()

                next_to_visit = []
                if coord.col > 0:
                    # move left. but if we're on the top or bottom row, we can't do this
                    next_to_visit.append(Coord(coord.row, coord.col-1))
                if coord.col < self.col_count - 1:
                    # move right
                    next_to_visit.append(Coord(coord.row, coord.col+1))
                if coord.row > 0:
                    # move up. but if we're on the left or right column, we can't do this
                    next_to_visit.append(Coord(coord.row-1, coord.col))
                if coord.row < self.row_count - 1:
                    # move down
                    next_to_visit.append(Coord(coord.row+1, coord.col))

                next_to_visit = [c for c in next_to_visit
                                 if c not in path
                                 and self.grid[c.row][c.col] in '.<>^v']
                for c in next_to_visit:
                    if c == end_pos:
                        # if we get to end_pos, then ensure nc is included in ret
                        ret.append(nc)
                        to_visit = []
                        break
                    else:
                        p = {c}
                        p.update(path)
                        to_visit.append((c, frozenset(p)))
        return ret

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
