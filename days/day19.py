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
        return "dayXX 2"

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
        print(f"{part}: in", end='')
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
                    print(f" -> {condition.workflow}", end='')
                    if condition.workflow == 'A':
                        print()
                        return True
                    elif condition.workflow == 'R':
                        print()
                        return False
                    else:
                        workflow = workflows[condition.workflow]
                        break
