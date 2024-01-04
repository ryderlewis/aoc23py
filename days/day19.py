from .day import Day
from collections import namedtuple

Part = namedtuple('Part', 'x m a s')
Condition = namedtuple('Condition', 'var comp val workflow', defaults=[None, None, None, None])
Workflow = namedtuple('Workflow', 'label conditions', defaults=[None, None])


class Day19(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        parts, workflows = self.parse()
        s = 0

        for part in parts:
            if self._accepted(part, workflows):
                s += sum(part)
        return str(s)

    def part2(self) -> str:
        _, workflows = self.parse()
        return str(Day19._count(workflows, 'in', range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)))

    @staticmethod
    def _count(workflows: dict[str, Workflow], curr: str, xrange: range, mrange: range, arange: range, srange: range) -> int:
        if curr == 'A':
            return len(xrange)*len(mrange)*len(arange)*len(srange)
        if curr == 'R':
            return 0

        count = 0
        workflow = workflows[curr]
        for condition in workflow.conditions:
            if condition.var is None:
                count += Day19._count(workflows, condition.workflow, xrange, mrange, arange, srange)
            else:
                if condition.var == 'x':
                    if condition.comp == '<':
                        new_xrange = Day19._range_overlap(xrange, range(1, condition.val))
                        xrange = Day19._range_overlap(xrange, range(condition.val, 4001))
                    else:
                        new_xrange = Day19._range_overlap(xrange, range(condition.val+1, 4001))
                        xrange = Day19._range_overlap(xrange, range(1, condition.val+1))
                    if new_xrange:
                        count += Day19._count(workflows, condition.workflow, new_xrange, mrange, arange, srange)
                elif condition.var == 'm':
                    if condition.comp == '<':
                        new_mrange = Day19._range_overlap(mrange, range(1, condition.val))
                        mrange = Day19._range_overlap(mrange, range(condition.val, 4001))
                    else:
                        new_mrange = Day19._range_overlap(mrange, range(condition.val+1, 4001))
                        mrange = Day19._range_overlap(mrange, range(1, condition.val+1))
                    if new_mrange:
                        count += Day19._count(workflows, condition.workflow, xrange, new_mrange, arange, srange)
                elif condition.var == 'a':
                    if condition.comp == '<':
                        new_arange = Day19._range_overlap(arange, range(1, condition.val))
                        arange = Day19._range_overlap(arange, range(condition.val, 4001))
                    else:
                        new_arange = Day19._range_overlap(arange, range(condition.val+1, 4001))
                        arange = Day19._range_overlap(arange, range(1, condition.val+1))
                    if new_arange:
                        count += Day19._count(workflows, condition.workflow, xrange, mrange, new_arange, srange)
                else:
                    if condition.comp == '<':
                        new_srange = Day19._range_overlap(srange, range(1, condition.val))
                        srange = Day19._range_overlap(srange, range(condition.val, 4001))
                    else:
                        new_srange = Day19._range_overlap(srange, range(condition.val+1, 4001))
                        srange = Day19._range_overlap(srange, range(1, condition.val+1))
                    if new_srange:
                        count += Day19._count(workflows, condition.workflow, xrange, mrange, arange, new_srange)
        return count

    @staticmethod
    def _range_overlap(a: range, b: range) -> range:
        return range(max(a.start, b.start), min(a.stop, b.stop)) or None

    def parse(self) -> tuple[tuple[Part, ...], dict[str, Workflow]]:
        parts = []
        workflows = {}

        for line in self.data_lines():
            if line == "":
                continue
            if line.startswith("{"):
                parts.append(self._parse_part(line))
            else:
                workflow = self._parse_workflow(line)
                workflows[workflow.label] = workflow

        return tuple(parts), workflows

    @staticmethod
    def _parse_part(line) -> Part:
        x, m, a, s = line[1:-1].split(',')
        return Part(x=int(x[2:]), m=int(m[2:]), a=int(a[2:]), s=int(s[2:]))

    @staticmethod
    def _parse_workflow(line) -> Workflow:
        label, rest = line.rstrip('}').split('{')
        conditions = []
        for c in rest.split(','):
            conditions.append(Day19._parse_condition(c))
        return Workflow(label=label, conditions=conditions)

    @staticmethod
    def _parse_condition(c: str) -> Condition:
        if ':' in c:
            equation, workflow = c.split(':')
            if '<' in equation:
                comp = '<'
            else:
                comp = '>'
            var, val = equation.split(comp)
            return Condition(var=var, val=int(val), comp=comp, workflow=workflow)
        else:
            return Condition(workflow=c)

    @staticmethod
    def _accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
        # print(f"{part}: in", end='')
        workflow = workflows['in']
        while True:
            for condition in workflow.conditions:

                if condition.var is None:
                    test = True
                else:
                    if condition.var == 'x':
                        pval = part.x
                    elif condition.var == 'm':
                        pval = part.m
                    elif condition.var == 'a':
                        pval = part.a
                    else:
                        pval = part.s

                    if condition.comp == '<':
                        test = pval < condition.val
                    else:
                        test = pval > condition.val

                if test:
                    # print(f" -> {condition.workflow}", end='')
                    if condition.workflow == 'A':
                        # print()
                        return True
                    elif condition.workflow == 'R':
                        # print()
                        return False
                    else:
                        workflow = workflows[condition.workflow]
                        break
