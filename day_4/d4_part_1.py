from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [list(line) for line in data.splitlines()]


def check_pos(row: int, col: int, grid: list[list[str]]) -> int:
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return 0

    return 1 if grid[row][col] == "@" else 0


def sum_pos(row: int, col: int, grid: list[list[str]]) -> int:
    total = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue

            total += check_pos(row + i, col + j, grid)

    return total


def task(data: str) -> int:
    grid = parse_input(data)

    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "@" and sum_pos(row, col, grid) < 4:
                total += 1

    return total


def test_example() -> None:
    assert task(read_file("day_4/test.txt")) == 13


def test_real() -> None:
    result = task(get_data(day=4, year=2025))
    print(result)
    assert result == 1569
