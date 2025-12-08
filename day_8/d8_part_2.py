from __future__ import annotations

import math

from aocd import get_data


class JunctionBox:
    def __init__(self, x: int, y: int, z: int, visited: bool = False) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.visited = visited
        self.pathId = -1
        self.connections = []

    def connect(self, other: JunctionBox) -> None:
        if other not in self.connections:
            self.connections.append(other)


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    points = []
    for line in data.splitlines():
        parts = line.split(",")
        points.append(JunctionBox(int(parts[0]), int(parts[1]), int(parts[2])))

    return points


def distance(p1: JunctionBox, p2: JunctionBox) -> float:
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)


def compute_pair_distances(points: list) -> list:
    distances = []

    for a in points:
        a.visited = True
        for b in points:
            if b.visited:
                continue

            dist = distance(a, b)
            distances.append((dist, a, b))

    distances.sort(key=lambda x: x[0])
    return distances


def reset_path_ids(points: list) -> None:
    for p in points:
        p.pathId = -1


def get_path_length(jb: JunctionBox, newId: int) -> int:
    if jb.pathId == newId:
        return 0

    jb.pathId = newId
    total = 1
    for c in jb.connections:
        total += get_path_length(c, newId)

    return total


def count_circuits(points: list) -> bool:
    id = 0
    paths = []
    reset_path_ids(points)
    for p in points:
        if p.pathId != -1:
            continue
        pathLength = get_path_length(p, id)
        paths.append(pathLength)
        id += 1

        if len(paths) > 1:
            return False

    return len(paths) == 1


def make_connections(points: list, pairs: list) -> int:
    for p in pairs:
        a = p[1]
        b = p[2]

        a.connect(b)
        b.connect(a)

        numCircuits = count_circuits(points)
        if numCircuits:
            return a.x * b.x

    return 0


def task(data: str) -> int:
    points = parse_input(data)
    pairs = compute_pair_distances(points)
    result = make_connections(points, pairs)
    return result


def test_example() -> None:
    assert task(read_file("day_8/test.txt")) == 25272


def test_real() -> None:
    result = task(get_data(day=8, year=2025))
    print(result)
    assert result == 59039696
