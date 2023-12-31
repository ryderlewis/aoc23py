from .day import Day


class Day05(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seeds = None
        self._seed_ranges = None
        self._maps = []

    def part1(self) -> str:
        self.parse()
        return str(min(self.location(s) for s in self._seeds))

    def part2(self) -> str:
        self.parse()
        return str(min(self.range_location(s) for s in self._seed_ranges))

    def location(self, seed) -> int:
        val = seed
        for curr_map in self._maps:
            for dest, source, length in curr_map:
                if source <= val < source + length:
                    val = dest + val - source
                    break
        return val

    def range_location(self, seed_range: range) -> int:
        ranges = [seed_range]
        for curr_map in self._maps:
            new_ranges = []
            for curr_range in ranges:
                r = curr_range
                for dest, source, length in curr_map:
                    if r.stop <= source or len(r) == 0:
                        # r ends before this map begins, and because the map is sorted,
                        # all the remaining entries will be after this one.
                        break
                    if r.start >= source + length:
                        # r does not overlap this map
                        continue

                    if r.start < source:
                        # lop off the part of r that is before the current source
                        new_ranges.append(range(r.start, source))
                        r = range(source, r.stop)

                    next_r = range(source + length, r.stop)
                    r = range(r.start, min(r.stop, source + length))
                    translated_start = dest + r.start - source
                    new_ranges.append(range(translated_start, translated_start + len(r)))
                    r = next_r

                if len(r) > 0:
                    new_ranges.append(r)
            ranges = new_ranges
        return min(r.start for r in ranges)

    def parse(self) -> None:
        lines = self.data_lines()
        self._seeds = tuple(map(int, lines.pop(0)[7:].split(' ')))
        self._seed_ranges = tuple(range(a, a+b) for a, b in zip(self._seeds[::2], self._seeds[1::2]))
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

        for m in self._maps:
            m.sort(key=lambda x: (x[1], x[2]))
