from .day import Day
from collections import namedtuple

Record = namedtuple('Record', ['sections', 'counts'])


class Day12(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        records = self.parse_records()
        s = 0
        for rec in records:
            ways = self.count_ways(rec, 0)
            print(f"{rec}: {ways}")
            s += ways
        return str(s)

    def part2(self) -> str:
        return "dayXX 2"

    def parse_records(self) -> list[Record]:
        ret = []
        for line in self.data_lines():
            record, counts = line.split()
            sections = tuple(x for x in record.split('.') if len(x) > 0)
            ret.append(Record(sections, tuple(map(int, counts.split(',')))))
        return ret

    @staticmethod
    def count_ways(rec: Record, depth: int) -> int:
        spaces = ' ' * depth * 2
        print(f"{spaces}CALLED: {rec}")
        if len(rec.counts) == 0:
            if all(s.strip('?') == '' for s in rec.sections):
                print(f"{spaces}HERE A1 {rec}")
                return 1
            else:
                print(f"{spaces}HERE A0 {rec}")
                return 0
        sections = rec.sections
        while len(sections) > 0 and len(sections[0]) < rec.counts[0]:
            if all(s == '?' for s in sections[0]):
                sections = sections[1:]
            else:
                print(f"{spaces}HERE B {rec}, {sections}")
                return 0
        if len(sections) == 0:
            print(f"{spaces}HERE C {rec}")
            return 0

        # for this first section, find all the possible ways that the exact count
        # of springs can appear
        ways = 0
        # allow for the possibility that the first section does not have any springs at all
        if all(s == '?' for s in sections[0]):
            print(f"{spaces}HERE D {rec}")
            ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts), depth+1)
        for i in range(len(sections[0])):
            test = sections[0][i:]
            print(f"{spaces}HERE E {rec}: {test}")
            if len(test) < rec.counts[0]:
                print(f"{spaces}HERE E2 {rec}: {test}")
                break
            elif len(test) == rec.counts[0]:
                print(f"{spaces}HERE E3 {rec}: {test}")
                ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts[1:]), depth+1)
            else:
                if test[rec.counts[0]] != '#':
                    section2 = test[rec.counts[0]+1:]
                    print(f"{spaces}HERE F {rec}: {test}, {section2}")
                    if len(section2) > 0:
                        ways += Day12.count_ways(Record(sections=(section2,)+sections[1:], counts=rec.counts[1:]), depth+1)
                    else:
                        ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts[1:]), depth+1)
                print(f"{spaces}HERE G {rec}: {ways}")
            if test[0] == '#':
                print(f"{spaces}HERE H {rec}: {test}")
                break
        return ways
