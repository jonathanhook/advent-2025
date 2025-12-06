from collections import defaultdict

from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    rows = data.splitlines()

    for i in range(0, len(rows)):
        rows[i] = rows[i] + " "

    problems = []
    lastBreak = 0
    for col in range(0, len(rows[0])):
        for row in range(0, len(rows)):
            val = rows[row][col]
            if val != " ":
                break
            elif row == len(rows) - 1:
                numbers = defaultdict(lambda: defaultdict(str))
                width = col - lastBreak
                height = len(rows) - 1
                for pc in range(lastBreak, lastBreak + width):
                    for pr in range(0, height):
                        digit = rows[pr][pc]
                        numbers[pr][pc - lastBreak] = "" if digit == " " else digit

                operator = rows[height][lastBreak]
                problems.append((operator, numbers))
                lastBreak = col + 1

    return problems


def solve_problem(p: defaultdict) -> int:
    operator = p[0]
    data = p[1]

    rows = len(data.keys())
    cols = max(len(row) for row in data.values())

    total = 0
    for c in range(0, cols):
        number = ""
        for r in range(0, rows):
            number += data[r][c]
        val = int(number)

        if total == 0 or operator == "+":
            total += val
        else:
            total *= val

    return total


def task(data: str) -> int:
    problems = parse_input(data)

    total = 0
    for p in problems:
        total += solve_problem(p)

    return total


def test_example() -> None:
    assert task(read_file("day_6/test.txt")) == 3263827


def test_real() -> None:
    result = task(get_data(day=6, year=2025))
    print(result)
    assert result == 7450962489289
