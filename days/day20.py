from .day import Day
from collections import namedtuple
from collections.abc import Iterable

Signal = namedtuple('Signal', 'source dest high')


class Module:
    def __init__(self, line: str):
        if ' -> ' in line:
            self.name, destinations = line.split(' -> ')
            self.destinations = destinations.split(', ')
        else:
            self.name = line
            self.destinations = []

    def add_source(self, source: str) -> None:
        pass

    def receive(self, signal: Signal) -> Iterable[Signal]:
        pass


class FlipFlop(Module):
    def __init__(self, line: str):
        super().__init__(line)
        self._on = False

    def receive(self, signal: Signal) -> Iterable[Signal]:
        if signal.high:
            return

        self._on = not self._on
        for d in self.destinations:
            yield Signal(self.name, d, self._on)


class Conjunction(Module):
    def __init__(self, line: str):
        super().__init__(line)
        self._sources = {}

    def add_source(self, source: str) -> None:
        if source not in self._sources:
            self._sources[source] = False  # low signal

    def receive(self, signal: Signal) -> Iterable[Signal]:
        self._sources[signal.source] = signal.high
        all_high = all(self._sources.values())

        for d in self.destinations:
            yield Signal(self.name, d, not all_high)


class Broadcast(Module):
    def __init__(self, line: str):
        super().__init__(line)

    def receive(self, signal: Signal) -> Iterable[Signal]:
        for d in self.destinations:
            yield Signal(self.name, d, signal.high)


class Day20(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        modules = self.make_modules()
        slow, shigh = 0, 0
        for _ in range(1000):
            low, high = self.push_button(modules)
            slow += low
            shigh += high
        return str(slow * shigh)

    def part2(self) -> str:
        return "day20 2"

    @staticmethod
    def push_button(modules) -> tuple[int, int]:
        low, high = 0, 0
        signals = [Signal('button', 'broadcaster', False)]
        while len(signals) > 0:
            signal = signals.pop(0)
            if signal.high:
                high += 1
            else:
                low += 1
            for relay_signal in modules[signal.dest].receive(signal):
                signals.append(relay_signal)

        return low, high

    def make_modules(self) -> dict[str, Module]:
        modules = {}
        for line in self.data_lines():
            if line.startswith('broadcaster '):
                m = Broadcast(line)
            elif line.startswith('%'):
                m = FlipFlop(line[1:])
            elif line.startswith('&'):
                m = Conjunction(line[1:])
            else:
                raise ValueError(f"Cannot parse: {line}")
            modules[m.name] = m

        target_only_modules = {}
        for m in modules.values():
            for d in m.destinations:
                if d in modules:
                    modules[d].add_source(m.name)
                else:
                    target_only_modules[d] = Broadcast(d)

        modules.update(target_only_modules)
        return modules
