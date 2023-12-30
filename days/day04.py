from .day import Day


class Day04(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = 0
        for card, winning, have in self.cards():
            matches = [h for h in have if h in winning]
            if len(matches) > 0:
                s += 2**(len(matches)-1)
        return str(s)

    def part2(self) -> str:
        cards = self.cards()
        copies = [len([h for h in have if h in winning]) for card, winning, have in cards]
        counts = [1 for _ in range(len(copies))]
        for i in range(len(counts)):
            for j in range(copies[i]):
                counts[i+j+1] += counts[i]
        return str(sum(counts))

    def cards(self) -> list[tuple]:
        ret = []
        for line in self.data_lines():
            a, c = line.split(' | ')
            a, b = a.split(': ')
            card = int(a[4:].strip())
            winning = tuple(int(n) for n in b.split(' ') if n != '')
            have = tuple(int(n) for n in c.split(' ') if n != '')
            ret.append((card, winning, have))
        return ret
