import math
from dataclasses import dataclass

from aocd import get_data


@dataclass
class JunctionBox:
    id: int
    x: int
    y: int
    z: int
    visited: bool = False
    circuit: int = -1


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def print_to_file(data: str, clear: bool = False) -> None:
    mode = "w" if clear else "a"
    with open("day_8/debug.txt", mode) as f:
        print(data, file=f)


def parse_input(data: str) -> list:
    points = []
    id = 0
    for line in data.splitlines():
        parts = line.split(",")
        points.append(JunctionBox(id, int(parts[0]), int(parts[1]), int(parts[2])))
        id += 1

    return points


def distance(p1: JunctionBox, p2: JunctionBox) -> float:
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)


def compute_distances(points: list) -> list:
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


def find_existing_circuit(a: JunctionBox, b: JunctionBox) -> int:
    if a.circuit != -1:
        return a.circuit
    elif b.circuit != -1:
        return b.circuit
    return -1


def consolodate_circuits() -> None:
    return


def solve(boxes: list, connections: int) -> int:
    connectionsMade = []
    idCounter = 0
    connectionCount = 0
    for i in range(0, len(boxes)):
        a = boxes[i][1]
        b = boxes[i][2]

        # if both already connected in the same circuit (pass)
        if a.circuit != -1 and b.circuit != -1 and a.circuit == b.circuit:
            continue

        # if both in different circuits (merge them)
        elif a.circuit != -1 and b.circuit != -1 and a.circuit != b.circuit:
            # replace all in b's circuit with a's circuit
            for j in range(len(boxes)):
                if boxes[j][1].circuit == b.circuit:
                    boxes[j][1].circuit = a.circuit
                if boxes[j][2].circuit == b.circuit:
                    boxes[j][2].circuit = a.circuit

        # if one or both not connected yet
        else:
            if a.circuit != -1:
                circuitId = a.circuit
            elif b.circuit != -1:
                circuitId = b.circuit
            else:
                circuitId = idCounter
                idCounter += 1

            boxes[i][1].circuit = circuitId
            boxes[i][2].circuit = circuitId

        # print_to_file(
        #     f"{connectionCount}:"
        #     f"{str(circuitId)}\t({boxes[i][1].x},{boxes[i][1].y},{boxes[i][1].z})-{boxes[i][1].circuit}:"
        #     f"({boxes[i][2].x},{boxes[i][2].y},{boxes[i][2].z}-{boxes[i][2].circuit})"
        # )

        connectionsMade.append(boxes[i])

        connectionCount += 1
        if connectionCount >= connections:
            break

    finalCircuits = {}
    for i in range(0, len(connectionsMade)):
        currentId = connectionsMade[i][1].circuit
        if currentId != -1:
            if currentId not in finalCircuits:
                finalCircuits[currentId] = set()
            finalCircuits[currentId].add(connectionsMade[i][1].id)
            finalCircuits[currentId].add(connectionsMade[i][2].id)

        print_to_file(
            f"{connectionsMade[i][1].id}({connectionsMade[i][1].x},{connectionsMade[i][1].y},{connectionsMade[i][1].z}){connectionsMade[i][1].circuit}:"
            f"{connectionsMade[i][2].id}({connectionsMade[i][2].x},{connectionsMade[i][2].y},{connectionsMade[i][2].z}){connectionsMade[i][2].circuit}"
        )

    # finalCircuits = {}

    # for i in range(0, len(boxes)):
    #     currentId = boxes[i][1].circuit
    #     if currentId != -1:
    #         if currentId not in finalCircuits:
    #             finalCircuits[currentId] = 0  # set()
    #         finalCircuits[currentId] += 1
    # finalCircuits[currentId].add((boxes[i][2].x, boxes[i][2].y, boxes[i][2].z))

    # print_to_file(
    #     f"{connectionCount}:"
    #     f"{str(circuitId)}\t({boxes[i][1].x},{boxes[i][1].y},{boxes[i][1].z})-{boxes[i][1].circuit}:"
    #     f"({boxes[i][2].x},{boxes[i][2].y},{boxes[i][2].z}-{boxes[i][2].circuit})"
    # )

    largest_three = sorted(finalCircuits.values(), reverse=True)[:3]
    result = 1
    for e in largest_three:
        result *= len(e)

    return result


def task(data: str, connections: int) -> int:
    points = parse_input(data)
    distances = compute_distances(points)

    print_to_file("", True)

    result = solve(distances, connections)

    return result


def test_example() -> None:
    # task(read_file("day_8/test.txt"), 10)
    assert task(read_file("day_8/test.txt"), 10) == 40


def test_real() -> None:
    result = task(get_data(day=8, year=2025), 1000)
    print(result)
    # assert result == 0
