from collections import defaultdict

from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    rows = data.splitlines()

    problems = []
    lastBreak = 0
    for col in range(0, len(rows[0])):
        for row in range(0, len(rows)):
            val = rows[row][col]
            if val != " ":
                break
            elif row == len(rows) - 1:
                # found break
                numbers = defaultdict(lambda: defaultdict(int))
                width = col - lastBreak
                height = len(rows) - 1
                for pc in range(lastBreak, width):
                    for pr in range(0, height):
                        if pr < len(rows) and pc < len(rows[pr]):
                            digit = rows[pc][pr]
                            numbers[pc][pr] = 0 if digit == " " else int(digit)
                        else:
                            numbers[pc][pr] = 0  # maybe not needed

                operator = rows[height][lastBreak]
                problems.append((operator, numbers))
                lastBreak = lastBreak + width
                print("jello")

    return []


def parse_problems(input: list) -> list:
    output = []
    for rowIndex in range(0, len(input)):
        row = input[rowIndex]
        for problemIndex in range(0, len(row)):
            problem = row[problemIndex]
            for columnIndex in range(0, len(problem)):
                column = problem[columnIndex]
                if problemIndex >= len(output):
                    output.append(defaultdict(lambda: defaultdict(int)))
                output[problemIndex][rowIndex][columnIndex] = column

    return output


def solve_problem(p: defaultdict) -> int:
    rows = len(p.keys()) - 1
    cols = max(len(row) for row in p.values())
    operator = p[rows][0]

    for c in range(0, cols):
        number = ""
        for r in range(0, rows):
            val = p[r][c]
            if val != 0:
                number += val
        print(number)

    return 0


def task(data: str) -> int:
    input = parse_input(data)
    problems = parse_problems(input)

    total = 0
    for p in problems:
        total += solve_problem(p)

    return total


def test_example() -> None:
    assert task(read_file("day_6/test.txt")) == 4277556


def test_real() -> None:
    result = task(get_data(day=6, year=2025))
    print(result)
    assert result == 4405895212738
