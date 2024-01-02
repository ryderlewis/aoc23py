from .day import Day
from collections import namedtuple
from functools import cache

Record = namedtuple('Record', ['sections', 'counts'])


class Day12(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        records = self.parse_records(1)
        return str(sum(self.count_ways(rec) for rec in records))

    def part2(self) -> str:
        records = self.parse_records(5)
        return str(sum(self.count_ways(rec) for rec in records))

    def parse_records(self, copies: int) -> list[Record]:
        ret = []
        for line in self.data_lines():
            record, counts = line.split()
            record = '?'.join([record for _ in range(copies)])
            counts = ','.join([counts for _ in range(copies)])
            sections = tuple(x for x in record.split('.') if len(x) > 0)
            ret.append(Record(sections, tuple(map(int, counts.split(',')))))
        return ret

    @staticmethod
    @cache
    def count_ways(rec: Record) -> int:
        if len(rec.counts) == 0:
            if all(s.strip('?') == '' for s in rec.sections):
                return 1
            else:
                return 0
        sections = rec.sections
        while len(sections) > 0 and len(sections[0]) < rec.counts[0]:
            if all(s == '?' for s in sections[0]):
                sections = sections[1:]
            else:
                return 0
        if len(sections) == 0:
            return 0

        # for this first section, find all the possible ways that the exact count
        # of springs can appear
        ways = 0
        # allow for the possibility that the first section does not have any springs at all
        if all(s == '?' for s in sections[0]):
            ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts))
        for i in range(len(sections[0])):
            test = sections[0][i:]
            if len(test) < rec.counts[0]:
                break
            elif len(test) == rec.counts[0]:
                ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts[1:]))
            else:
                if test[rec.counts[0]] != '#':
                    section2 = test[rec.counts[0]+1:]
                    if len(section2) > 0:
                        ways += Day12.count_ways(Record(sections=(section2,)+sections[1:], counts=rec.counts[1:]))
                    else:
                        ways += Day12.count_ways(Record(sections=sections[1:], counts=rec.counts[1:]))
            if test[0] == '#':
                break
        return ways
