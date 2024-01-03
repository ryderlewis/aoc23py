from .day import Day


class Day15(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        return str(sum(self.hash(s) for s in self.sequence()))

    def part2(self) -> str:
        boxes = [[] for _ in range(256)]
        for s in self.sequence():
            if '=' in s:
                label, focus = s.split('=')
                focus = int(focus)
                box = self.hash(label)
                arr = boxes[box]
                found = False
                for pos in range(len(arr)):
                    if arr[pos][0] == label:
                        arr[pos] = (label, focus)
                        found = True
                        break
                if not found:
                    arr.append((label, focus))
            else:
                label = s.rstrip('-')
                box = self.hash(label)
                arr = boxes[box]
                for pos in range(len(arr)):
                    if arr[pos][0] == label:
                        arr.pop(pos)
                        break

        s = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                s += (i+1) * (j+1) * lens[1]
        return str(s)

    def sequence(self) -> tuple[str, ...]:
        return tuple(self.data_lines().pop(0).split(','))

    @staticmethod
    def hash(s: str) -> int:
        val = 0
        for c in s:
            val += ord(c)
            val *= 17
            val %= 256
        return val
