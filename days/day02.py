from .day import Day


class Day02(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = 0
        for x in self.data_lines():
            game, rgbs = self.parse_line(x)
            if all(r <= 12 and g <= 13 and b <= 14 for r, g, b in rgbs):
                s += game
        return str(s)

    def part2(self) -> str:
        p = 0
        for x in self.data_lines():
            mr, mg, mb = 0, 0, 0
            game, rgbs = self.parse_line(x)
            for r, g, b in rgbs:
                mr = max(mr, r)
                mg = max(mg, g)
                mb = max(mb, b)
            p += mr * mg * mb
        return str(p)

    def parse_line(self, line) -> tuple:
        # returns tuple of (game number, [(r,g,b), (r,g,b)])
        # Game 14: 18 green, 6 blue, 5 red; 5 blue, 15 red, 19 green; 7 green, 11 blue, 20 red; 5 red, 18 green, 7 blue
        game, rest = line.split(': ')
        game = int(game[5:])
        rgbs = []
        for s in rest.split('; '):
            r, g, b = 0, 0, 0
            for c in s.split(', '):
                quantity, color = c.split(' ')
                if color == 'red':
                    r += int(quantity)
                elif color == 'green':
                    g += int(quantity)
                elif color == 'blue':
                    b += int(quantity)
                else:
                    raise Exception(f"unrecognized color: {color}")
            rgbs.append((r, g, b))
        return int(game), rgbs
