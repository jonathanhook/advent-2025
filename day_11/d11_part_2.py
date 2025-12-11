from __future__ import annotations

from aocd import get_data


class Node:
    def __init__(self, id: str) -> None:
        self.id = id
        self.connections: list[Node] = []

    def connect(self, n: Node) -> None:
        self.connections.append(n)


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    nodes = []
    for line in data.splitlines():
        parts = line.split(" ")
        id = parts[0][:-1]
        connections = parts[1:]
        nodes.append((id, connections))

    return nodes


def build_graph(nodeData: list) -> Node:
    nodes = {}
    nodes["out"] = Node("out")
    for nd in nodeData:
        id = nd[0]
        nodes[id] = Node(id)

    for nd in nodeData:
        id = nd[0]
        current = nodes[id]
        for toConnect in nd[1]:
            current.connect(nodes[toConnect])

    return nodes["svr"]


def find_unique_paths(current: Node, fft: bool, dac: bool, seen: dict) -> int:
    if current.id == "out":
        return 1 if fft and dac else 0

    _fft = True if current.id == "fft" else fft
    _dac = True if current.id == "dac" else dac

    key = (current.id, _fft, _dac)
    if key in seen:
        return seen[key]

    total = 0
    for child in current.connections:
        total += find_unique_paths(child, _fft, _dac, seen)

    seen[key] = total
    return total


def task(data: str) -> int:
    nodeData = parse_input(data)
    svr = build_graph(nodeData)
    count = find_unique_paths(svr, False, False, {})
    return count


def test_example() -> None:
    assert task(read_file("day_11/test_p2.txt")) == 2


def test_real() -> None:
    result = task(get_data(day=11, year=2025))
    print(result)
    assert result == 511378159390560
