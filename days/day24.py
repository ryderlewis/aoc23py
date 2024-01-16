from .day import Day
from fractions import Fraction


class Entry:
    def __init__(self, line: str):
        vals = line.split()
        self.px = int(vals.pop(0).rstrip(','))
        self.py = int(vals.pop(0).rstrip(','))
        self.pz = int(vals.pop(0).rstrip(','))
        _ = vals.pop(0)
        self.vx = int(vals.pop(0).rstrip(','))
        self.vy = int(vals.pop(0).rstrip(','))
        self.vz = int(vals.pop(0).rstrip(','))

    def intersect_2d(self, other) -> type[tuple[int, int], None]:
        # find (x, y) coordinate where self intersects with other
        m_self, b_self = self.m_and_b_2d()
        m_other, b_other = other.m_and_b_2d()
        if m_self is None or b_self is None or m_self == m_other:
            return None

        # where do two lines intersect, based on formula?
        # y = m1x+b1
        # y = m2x+b2
        # y - m1x - b1 = 0
        # y - m2x - b2 = 0
        # 0 - m1x + m2x - b1 + b2 = 0
        # (m2-m1)x = b1-b2
        # x = (b1-b2)/(m2-m1)
        ix = (b_self-b_other)/(m_other-m_self)
        iy = ix * m_self + b_self

        # make sure intersection is in the future
        if ix >= self.px and self.vx < 0:
            return None
        if ix <= self.px and self.vx > 0:
            return None
        if iy >= self.py and self.vy < 0:
            return None
        if iy <= self.py and self.vy > 0:
            return None
        if ix >= other.px and other.vx < 0:
            return None
        if ix <= other.px and other.vx > 0:
            return None
        if iy >= other.py and other.vy < 0:
            return None
        if iy <= other.py and other.vy > 0:
            return None

        return ix, iy

    def m_and_b_2d(self) -> type[tuple[Fraction, int], tuple[None, None]]:
        # y = mx + b
        # y = (vy/vx)x + b
        # b = y - (vy/vx)x
        if self.vx == 0:
            return None, None
        m = Fraction(self.vy, self.vx)
        b = self.py - m * self.px
        return m, b

    def __str__(self) -> str:
        return f"Entry(pos=({self.px}, {self.py}, {self.pz}) vel=({self.vx}, {self.vy}, {self.vz})"


class Day24(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        entries = self.entries()
        i_count_test = 0
        i_count_real = 0
        for i in range(len(entries)):
            for j in range(i+1, len(entries)):
                intersect = entries[i].intersect_2d(entries[j])
                print(f"{entries[i]} intersect {entries[j]} at {intersect}")
                if intersect is not None and 7 <= intersect[0] <= 27 and 7 <= intersect[1] <= 27:
                    i_count_test += 1
                if intersect is not None and 200000000000000 <= intersect[0] <= 400000000000000 and 200000000000000 <= intersect[1] <= 400000000000000:
                    i_count_real += 1
        print(f"test={i_count_test}")
        return str(i_count_real)

    def part2(self) -> str:
        return "day24 2"

    def entries(self) -> tuple[Entry, ...]:
        return tuple([Entry(line) for line in self.data_lines()])
