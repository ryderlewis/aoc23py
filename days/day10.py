from .day import Day


class Maze:
    def __init__(self, inputs: list[str]):
        self._coords = {}
        self._rows = len(inputs)
        self._cols = len(inputs[0])
        for row, line in enumerate(inputs):
            for col, char in enumerate(line):
                if char == 'S':
                    self._start = (row, col)
                else:
                    self._coords[(row, col)] = char
        # replace start with the appropriate character
        srow, scol = self._start
        if self.can_left(srow, scol+1):
            if self.can_right(srow, scol-1):
                self._coords[self._start] = '-'
            elif self.can_up(srow+1, scol):
                self._coords[self._start] = 'F'
            else:
                self._coords[self._start] = 'L'
        elif self.can_right(srow, scol-1):
            if self.can_up(srow+1, scol):
                self._coords[self._start] = '7'
            else:
                self._coords[self._start] = 'J'
        elif self.can_up(srow+1, scol):
            # below start can go up, the only option remaining is that above can down.
            self._coords[self._start] = '|'

    def max_distance(self) -> int:
        return max(self.main_pipe().values())

    def inside_count(self) -> int:
        pipe_coords = set()
        for prow, pcol in self.main_pipe().keys():
            pipe_coords.add((prow, pcol))
            if self.can_right(prow, pcol):
                pipe_coords.add((prow, pcol+0.5))
            if self.can_down(prow, pcol):
                pipe_coords.add((prow+0.5, pcol))

        non_pipe_coords = set()
        row = -0.5
        while row < self._rows:
            col = -0.5
            while col < self._cols:
                crow = row if row % 1 == 0.5 else int(row)
                ccol = col if col % 1 == 0.5 else int(col)
                coord = (crow, ccol)
                if coord not in pipe_coords:
                    non_pipe_coords.add(coord)
                col += 0.5
            row += 0.5

        visited = set()
        to_visit = [(-0.5, -0.5)]
        while len(to_visit) > 0:
            coord = to_visit.pop(0)
            visited.add(coord)
            up_row = coord[0]-0.5 if coord[0] % 1 == 0 else int(coord[0]-0.5)
            left_col = coord[1]-0.5 if coord[1] % 1 == 0 else int(coord[1]-0.5)
            up = (up_row, coord[1])
            down = (up_row+1, coord[1])
            left = (coord[0], left_col)
            right = (coord[0], left_col+1)
            if up in non_pipe_coords and up not in visited:
                to_visit.append(up)
                visited.add(up)
            if down in non_pipe_coords and down not in visited:
                to_visit.append(down)
                visited.add(down)
            if left in non_pipe_coords and left not in visited:
                to_visit.append(left)
                visited.add(left)
            if right in non_pipe_coords and right not in visited:
                to_visit.append(right)
                visited.add(right)

        return len([c for c in non_pipe_coords if c[0] % 1 == 0 and c[1] % 1 == 0 and c not in visited])

    def main_pipe(self) -> dict[tuple[int, int], int]:
        # do a BFS
        visited = {}
        to_visit = [(self._start, 0)]
        while len(to_visit) > 0:
            coord, dist = to_visit.pop(0)
            visited[coord] = dist
            if self.can_up(*coord) and (coord[0]-1, coord[1]) not in visited:
                to_visit.append(((coord[0]-1, coord[1]), dist+1))
            if self.can_down(*coord) and (coord[0]+1, coord[1]) not in visited:
                to_visit.append(((coord[0]+1, coord[1]), dist+1))
            if self.can_left(*coord) and (coord[0], coord[1]-1) not in visited:
                to_visit.append(((coord[0], coord[1]-1), dist+1))
            if self.can_right(*coord) and (coord[0], coord[1]+1) not in visited:
                to_visit.append(((coord[0], coord[1]+1), dist+1))
        return visited

    def can_left(self, row: int, col: int) -> bool:
        try:
            return self._coords[(row, col)] in '-J7'
        except KeyError:
            return False

    def can_right(self, row: int, col: int) -> bool:
        try:
            return self._coords[(row, col)] in '-LF'
        except KeyError:
            return False

    def can_up(self, row: int, col: int) -> bool:
        try:
            return self._coords[(row, col)] in '|LJ'
        except KeyError:
            return False

    def can_down(self, row: int, col: int) -> bool:
        try:
            return self._coords[(row, col)] in '|7F'
        except KeyError:
            return False


class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        maze = Maze(self.data_lines())
        return str(maze.max_distance())

    def part2(self) -> str:
        maze = Maze(self.data_lines())
        return str(maze.inside_count())
