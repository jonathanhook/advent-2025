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
                print(grid[i][j], end="", file=f)
            print("", file=f)


def find_start(grid: list) -> tuple[int, int]:
    for i in range(0, len(grid[0])):
        if grid[0][i] == "S":
            return (i, 0)
    return (0, 0)


def traverse(pos: tuple[int, int], grid: list, visited: list, splits: set) -> None:
    x = pos[0]
    y = pos[1]

    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return

    visited.append((x, y))
    val = grid[y][x]

    if val == "^":
        if tuple(visited) not in splits:
            splits.add(tuple(visited))

            traverse((x - 1, y), grid, visited.copy(), splits)
            traverse((x + 1, y), grid, visited.copy(), splits)
    else:
        traverse((x, y + 1), grid, visited, splits)


def task(data: str) -> int:
    grid = parse_input(data)
    start = find_start(grid)

    visited = []
    splits = set()
    traverse(start, grid, visited, splits)

    print_grid(grid)

    return len(splits) + 1


def test_example() -> None:
    print("GELLO")
    assert task(read_file("day_7/test.txt")) == 40


def test_real() -> None:
    result = task(get_data(day=7, year=2025))
    print(result)
    # assert result == 1619
