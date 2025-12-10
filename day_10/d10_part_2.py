import copy
from collections import deque

from aocd import get_data


class Machine:
    def __init__(self, target: list[int], buttons: list[list[int]]):
        self.target: list[int] = target
        self.buttons: list[list[int]] = buttons
        self.state: list[int] = [0] * len(self.target)

    def press_button(self, id: int) -> None:
        toPress = self.buttons[id]
        for b in toPress:
            self.state[b] += 1

    def is_started(self) -> bool:
        return self.state == self.target


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list[Machine]:
    machines = []
    for line in data.splitlines():
        parts = line.split(" ")

        target = [
            int(x) for x in parts[-1].replace("{", "").replace("}", "").split(",")
        ]

        buttons = []
        for b in parts[1:-1]:
            schematic = [int(x) for x in b.replace("(", "").replace(")", "").split(",")]
            buttons.append(schematic)

        machines.append(Machine(target, buttons))

    return machines


def bfs(machine: Machine) -> int:
    queue = deque()
    queue.append((0, machine, -1))

    seen = set()
    while len(queue) > 0:
        current = queue.popleft()
        pressesSoFar = current[0]
        currentMachine = current[1]
        toPress = current[2]

        if toPress != -1:
            currentMachine.press_button(toPress)

        hash = tuple(currentMachine.state)
        if hash in seen:
            continue
        seen.add(hash)

        if currentMachine.is_started():
            return pressesSoFar

        for bId in range(len(currentMachine.buttons)):
            machineCopy = copy.deepcopy(currentMachine)
            queue.append((pressesSoFar + 1, machineCopy, bId))

    return -1


def task(data: str) -> int:
    machines = parse_input(data)

    result = 0
    for m in machines:
        result += bfs(m)

    return result


def test_example() -> None:
    assert task(read_file("day_10/test.txt")) == 33


def test_real() -> None:
    result = task(get_data(day=10, year=2025))
    print(result)
    assert result == 538
