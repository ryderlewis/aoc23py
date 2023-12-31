from .day import Day
from collections import Counter
from functools import total_ordering


@total_ordering
class Hand:
    def __init__(self, *, cards, bid):
        self.cards = cards
        self.bid = bid
        self._hand_type = None
        self._order = None
        self.__parse()

    def __parse(self) -> None:
        self._hand_type = self.__hand_type()
        self._order = self.__order()

    def __lt__(self, other) -> bool:
        if self._hand_type != other._hand_type:
            return self._hand_type < other._hand_type
        return self._order > other._order

    def __hand_type(self) -> int:
        c = Counter(self.cards)
        if len(c) == 5:
            return 7  # high card
        elif len(c) == 4:
            return 6  # pair
        elif len(c) == 3:
            if max(c.values()) == 2:
                return 5  # two pair
            else:
                return 4  # three of a kind
        elif len(c) == 2:
            if max(c.values()) == 3:
                return 3  # full house
            else:
                return 2  # four of a kind
        else:
            return 1  # five of a kind

    def __order(self) -> tuple:
        vals = []
        for c in self.cards:
            if '2' <= c <= '9':
                vals.append(int(c))
            elif c == 'T':
                vals.append(10)
            elif c == 'J':
                vals.append(11)
            elif c == 'Q':
                vals.append(12)
            elif c == 'K':
                vals.append(13)
            elif c == 'A':
                vals.append(14)
            else:
                raise ValueError(f"unknown card: {c}")
        return tuple(vals)


class Day07(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        hands = self.hands()
        s = 0
        for r, h in enumerate(sorted(hands, reverse=True), 1):
            s += r * h.bid
        return str(s)

    def part2(self) -> str:
        return "dayXX 2"

    def hands(self) -> list[Hand]:
        hands = []
        for line in self.data_lines():
            cards, bid = line.split()
            hands.append(Hand(cards=cards, bid=int(bid)))
        return hands
