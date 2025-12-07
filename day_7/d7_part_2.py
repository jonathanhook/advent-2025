from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [list(line) for line in data.splitlines()]


def print_grid(grid: list) -> None:
    with open("day_7/debug.txt", "w") as f:
        print("", file=f)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                print(grid[i][j], end="\t", file=f)
            print("", file=f)


def get_result(grid: list) -> int:
    total = 0
    for i in range(0, len(grid[0])):
        val = grid[len(grid) - 1][i]
        if val != ".":
            total += int(val)

    return total


def parse_val(val: str) -> int:
    if val == "." or val == "^":
        return 0
    elif val == "S":
        return 1
    else:
        return int(val)


def solve(grid: list) -> int:
    for row in range(1, len(grid)):
        for col in range(0, len(grid[0])):
            if grid[row][col] == "^":
                continue

            val = 0
            # above
            val += parse_val(grid[row - 1][col])

            # above-left
            if col > 0 and grid[row][col - 1] == "^":
                val += parse_val(grid[row - 1][col - 1])

            # above-right
            if col < len(grid[0]) - 2 and grid[row][col + 1] == "^":
                val += parse_val(grid[row - 1][col + 1])

            if val > 0:
                grid[row][col] = str(val)

    return 0


def task(data: str) -> int:
    grid = parse_input(data)
    solve(grid)

    print_grid(grid)

    return get_result(grid)


def test_example() -> None:
    assert task(read_file("day_7/test.txt")) == 40


def test_real() -> None:
    result = task(get_data(day=7, year=2025))
    print(result)
    assert result == 23607984027985
