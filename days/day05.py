from .day import Day


class Day05(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seeds = None
        self._maps = []

    def part1(self) -> str:
        self.parse()
        return str(min(self.location(s) for s in self._seeds))

    def part2(self) -> str:
        return "day05 2"

    def location(self, seed) -> int:
        val = seed
        for curr_map in self._maps:
            for dest, source, length in curr_map:
                if source <= val < source + length:
                    val = dest + val - source
                    break
        return val

    def parse(self) -> None:
        lines = self.data_lines()
        self._seeds = tuple(map(int, lines.pop(0)[7:].split(' ')))
        self._maps = []
        last_map = None

        for line in lines:
            if line == "":
                continue
            elif 'map:' in line:
                last_map = []
                self._maps.append(last_map)
            else:
                last_map.append(tuple(map(int, line.split(' '))))
