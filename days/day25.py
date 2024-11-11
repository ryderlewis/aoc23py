from .day import Day
import random


class Node:
    def __init__(self, name: str):
        self.names = {name}
        self.connections: dict["Node", int] = {}

    def add_connection(self, other: "Node", weight: int = 1):
        self.connections[other] = weight
        other.connections[self] = weight

    def total_edge_weight(self) -> int:
        return sum(self.connections.values())

    def merge_into_neighbor(self):
        # find a random neighbor and remove it from self's connections
        into: Node = random.choice(list(self.connections.keys()))
        into.connections.pop(self)
        into.names.update(self.names)
        self.connections.pop(into)

        # anything self is connected to is now connected to into
        while self.connections:
            node, weight = self.connections.popitem()
            node.connections.pop(self)
            if node in into.connections:
                into.connections[node] += weight
            else:
                into.connections[node] = weight
            node.connections[into] = into.connections[node]


class Graph:
    def __init__(self, data: list[str]):
        node_dict: dict[str, Node] = {}
        for d in data:
            l, rs = d.split(':')
            for r in rs.strip().split():
                l_node = node_dict.setdefault(l, Node(l))
                r_node = node_dict.setdefault(r, Node(r))
                l_node.add_connection(r_node)
        self.nodes: list[Node] = list(node_dict.values())

    def reduce(self) -> tuple[int, int, int]:
        while len(self.nodes) > 2:
            idx = random.randrange(len(self.nodes))
            node = self.nodes.pop(idx)
            node.merge_into_neighbor()
        print(f"reduced, remaining weight: {self.nodes[0].total_edge_weight()}")
        return len(self.nodes[0].names), len(self.nodes[1].names), self.nodes[0].total_edge_weight()


class Day25(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        while True:
            g = Graph(self.data_lines())
            a, b, w = g.reduce()
            if w <= 3:
                print(f"{a=}, {b=}, {w=}")
                return f"{a*b}"

    def part2(self) -> str:
        g = Graph(self.data_lines())
        return ""
