from .day import Day


class Day21(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        maze = self.maze()
        rows = len(maze)
        cols = len(maze[0])
        to_visit = []
        visited = {}
        for r in range(rows):
            for c in range(cols):
                if maze[r][c] == 'S':
                    to_visit.append((r, c, 0))
                    visited[(r, c)] = 0
                    break
            if len(to_visit):
                break

        # starting position is the one to_visit
        # do a BFS and count any spots that are multiples of 2 away from S
        while len(to_visit):
            r, c, count = to_visit.pop(0)
            if r-1 >= 0 and (r-1, c) not in visited and count < 64 and maze[r-1][c] == '.':
                to_visit.append((r-1, c, count+1))
                visited[(r-1, c)] = count+1
            if r+1 < rows and (r+1, c) not in visited and count < 64 and maze[r+1][c] == '.':
                to_visit.append((r+1, c, count+1))
                visited[(r+1, c)] = count+1
            if c-1 >= 0 and (r, c-1) not in visited and count < 64 and maze[r][c-1] == '.':
                to_visit.append((r, c-1, count+1))
                visited[(r, c-1)] = count+1
            if c+1 < cols and (r, c+1) not in visited and count < 64 and maze[r][c+1] == '.':
                to_visit.append((r, c+1, count+1))
                visited[(r, c+1)] = count+1

        return str(len([1 for v in visited.values() if v % 2 == 0]))

    def part2(self) -> str:
        return "dayXX 2"

    def maze(self) -> list[list[str]]:
        return [list(x) for x in self.data_lines()]
