from .day import Day
from collections import namedtuple
from collections.abc import Iterable
from copy import deepcopy

Coord = namedtuple('Coord', 'x y z')


class Brick:
    def __init__(self, identifier: str, start_coord: Coord, end_coord: Coord):
        s, e = sorted([start_coord, end_coord])
        self.identifier = identifier
        self.start_coord = s
        self.end_coord = e

    def volume(self) -> int:
        xl = abs(self.start_coord.x - self.end_coord.x)
        yl = abs(self.start_coord.y - self.end_coord.y)
        zl = abs(self.start_coord.z - self.end_coord.z)

        lengths = sorted([xl, yl, zl])
        if lengths[0] != 0 or lengths[1] != 0:
            raise Exception(f"Unexpected: {self.start_coord}, {self.end_coord}")

        return lengths[-1] + 1

    def coords(self) -> Iterable[Coord]:
        for x in range(self.start_coord.x, self.end_coord.x+1):
            for y in range(self.start_coord.y, self.end_coord.y+1):
                for z in range(self.start_coord.z, self.end_coord.z+1):
                    yield Coord(x, y, z)

    def fall_coords(self) -> Iterable[Coord]:
        for x in range(self.start_coord.x, self.end_coord.x+1):
            for y in range(self.start_coord.y, self.end_coord.y+1):
                for z in range(self.start_coord.z, self.end_coord.z+1):
                    yield Coord(x, y, z-1)

    def can_fall(self) -> bool:
        return self.min_z() > 1

    def fall(self) -> None:
        self.start_coord = self.start_coord._replace(z=self.start_coord.z-1)
        self.end_coord = self.end_coord._replace(z=self.end_coord.z-1)

    def min_x(self) -> int:
        return min(self.start_coord.x, self.end_coord.x)

    def max_x(self) -> int:
        return max(self.start_coord.x, self.end_coord.x)

    def min_y(self) -> int:
        return min(self.start_coord.y, self.end_coord.y)

    def max_y(self) -> int:
        return max(self.start_coord.y, self.end_coord.y)

    def min_z(self) -> int:
        return min(self.start_coord.z, self.end_coord.z)

    def max_z(self) -> int:
        return max(self.start_coord.z, self.end_coord.z)


class Day22(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        bricks = self.parse()

        fell = True
        while fell:
            fell = False
            for bi, brick in enumerate(bricks):
                all_coords = set()
                for b in [x for i, x in enumerate(bricks) if i != bi]:
                    all_coords.update(b.coords())
                while brick.can_fall() and not any(fc in all_coords for fc in brick.fall_coords()):
                    fell = True
                    print(f"hi ryder: {brick.identifier}")
                    brick.fall()

        for b in bricks:
            print(f"{b.identifier}: {b.start_coord}, {b.end_coord}")

        supports = {}
        for bi, brick in enumerate(bricks):
            # find out if this brick is holding up any other bricks
            brick_coords = set(brick.coords())
            supports[brick.identifier] = set()
            for b in [x for i, x in enumerate(bricks) if i != bi]:
                if b.can_fall() and any(fc in brick_coords for fc in b.fall_coords()):
                    supports[brick.identifier].add(b.identifier)

        supported_by = {b.identifier: set() for b in bricks}
        for a, a_supports in supports.items():
            for b in a_supports:
                if b not in supported_by:
                    supported_by[b] = set()
                supported_by[b].add(a)
        print(f"{supports}")
        print(f"{supported_by}")

        can_disintegrate = 0
        for b, s in supports.items():
            if len(s) == 0:
                # b doesn't support any other bricks
                can_disintegrate += 1
            else:
                # b supports other bricks - let's see if any _other_ bricks support the same bricks
                sole_supporter = False
                for supported in s:
                    all_supporters = supported_by[supported]
                    if len(all_supporters) == 1:
                        sole_supporter = True
                        break
                if not sole_supporter:
                    can_disintegrate += 1
        return str(can_disintegrate)

    def part2(self) -> str:
        bricks = self.parse()

        fell = True
        while fell:
            fell = False
            for bi, brick in enumerate(bricks):
                all_coords = set()
                for b in [x for i, x in enumerate(bricks) if i != bi]:
                    all_coords.update(b.coords())
                while brick.can_fall() and not any(fc in all_coords for fc in brick.fall_coords()):
                    fell = True
                    print(f"hi ryder: {brick.identifier}")
                    brick.fall()

        how_many_fall = 0
        for bi in range(len(bricks)):
            bricks_copy = []
            for i, b in enumerate(bricks):
                if i != bi:
                    bricks_copy.append(Brick(b.identifier, b.start_coord, b.end_coord))
            how_many_fall += self.fall_count(bricks[bi].identifier, tuple(bricks_copy))

        return str(how_many_fall)

    @staticmethod
    def fall_count(identifier: str, bricks: tuple[Brick, ...]) -> int:
        fall_ids = set()
        fell = True
        while fell:
            fell = False
            for bi, brick in enumerate(bricks):
                all_coords = set()
                for b in [x for i, x in enumerate(bricks) if i != bi]:
                    all_coords.update(b.coords())
                while brick.can_fall() and not any(fc in all_coords for fc in brick.fall_coords()):
                    fell = True
                    brick.fall()
                    fall_ids.add(brick.identifier)
        print(f"fall_count {identifier}: {len(fall_ids)}")
        return len(fall_ids)

    def parse(self) -> tuple[Brick, ...]:
        bricks = []
        for i, line in enumerate(self.data_lines()):
            start, end = line.split('~')
            sc = Coord(*map(int, start.split(',')))
            ec = Coord(*map(int, end.split(',')))
            identifier = str(i)
            bricks.append(Brick(identifier, sc, ec))
        return tuple(bricks)
