from .day import Day


class Maze:
    def __init__(self, inputs: list[str]):
        self._coords = {}
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
        # do a BFS and return the max value
        visited = set()
        to_visit = [(self._start, 0)]
        dist = 0
        while len(to_visit) > 0:
            coord, dist = to_visit.pop(0)
            visited.add(coord)
            if self.can_up(*coord) and (coord[0]-1, coord[1]) not in visited:
                to_visit.append(((coord[0]-1, coord[1]), dist+1))
            if self.can_down(*coord) and (coord[0]+1, coord[1]) not in visited:
                to_visit.append(((coord[0]+1, coord[1]), dist+1))
            if self.can_left(*coord) and (coord[0], coord[1]-1) not in visited:
                to_visit.append(((coord[0], coord[1]-1), dist+1))
            if self.can_right(*coord) and (coord[0], coord[1]+1) not in visited:
                to_visit.append(((coord[0], coord[1]+1), dist+1))
        return dist

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
        return "day10 2"
