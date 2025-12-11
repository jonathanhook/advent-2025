from aocd import get_data
from pulp import LpInteger, LpMinimize, LpProblem, LpVariable, lpSum


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list[tuple]:
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

        machines.append((target, buttons))

    return machines


def task(data: str) -> int:
    machines = parse_input(data)

    totalPresses = 0
    for m in machines:
        target = m[0]
        buttons = m[1]

        prob = LpProblem("Day 10 Part 2", LpMinimize)

        x = [
            LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(len(buttons))
        ]
        prob += lpSum(x)

        for i in range(len(target)):
            involvedButtons = []
            for j in range(len(buttons)):
                b = buttons[j]
                if i in b:
                    involvedButtons.append(j)

            prob += lpSum([x[j] for j in involvedButtons]) == target[i]

        prob.solve()

        presses = 0
        for v in prob.variables():
            if v.varValue is not None:
                presses += int(v.varValue)
        totalPresses += presses

    return totalPresses


def test_example() -> None:
    assert task(read_file("day_10/test.txt")) == 33


def test_real() -> None:
    result = task(get_data(day=10, year=2025))
    print(result)
    assert result == 20298
