from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in line.split(",")[:2]) for line in data.splitlines()]


def print_grid(grid: list) -> None:
    with open("day_9/debug.txt", "w") as f:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                print(grid[i][j], end="", file=f)
            print("", file=f)


def get_min_max(coords: list) -> tuple:
    min_x = min(t[0] for t in coords)
    min_y = min(t[1] for t in coords)
    max_x = max(t[0] for t in coords) + 1
    max_y = max(t[1] for t in coords) + 1

    return (min_x, min_y, max_x, max_y)


def get_grid(coords: list, minMax: tuple) -> list:
    min_x = minMax[0]
    min_y = minMax[1]
    max_x = minMax[2]
    max_y = minMax[3]

    grid = [["." for _ in range(max_x - min_x)] for _ in range(max_y - min_y)]

    for c in coords:
        x = c[0] - min_x
        y = c[1] - min_y
        grid[y][x] = "#"

    return grid


def inside(grid: list, start: tuple[int, int]) -> bool:
    nsew = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    direction = 0
    while direction < 4:
        pos = start
        while True:
            nx = pos[0] + nsew[direction][0]
            ny = pos[1] + nsew[direction][1]

            if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
                return False
            elif grid[ny][nx] == "#" or grid[ny][nx] == "X":
                direction += 1
                break
            else:
                pos = (nx, ny)

    return True


def fill(grid: list) -> None:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "X" or grid[row][col] == "#":
                continue

            if inside(grid, (col, row)):
                grid[row][col] = "X"


def draw_line(grid: list, start: tuple[int, int], end: tuple[int, int]) -> None:
    for x in range(min(start[0], end[0]) + 1, max(start[0], end[0])):
        grid[start[1]][x] = "X"

    for y in range(min(start[1], end[1]) + 1, max(start[1], end[1])):
        grid[y][start[0]] = "X"


def find_perimeter(grid: list) -> None:
    nsew = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    direction = 0
    start = (9, 6)  # hardcoded for test
    pos = start
    while direction < 4:
        # move in direction
        nx = pos[0] + nsew[direction][0]
        ny = pos[1] + nsew[direction][1]

        # if out of bounds or previously marked reset and look in new direction
        if (
            nx < 0
            or nx >= len(grid[0])
            or ny < 0
            or ny >= len(grid)
            or grid[ny][nx] == "X"
        ):
            pos = start
            direction += 1

        # else if found a coord
        elif grid[ny][nx] == "#":
            pos = (nx, ny)
            draw_line(grid, start, pos)
            start = pos
            direction = 0

        # else progress
        else:
            pos = (nx, ny)

    return


def check_allowed(grid: list, a: tuple, b: tuple, minMax: tuple) -> bool:
    mx = minMax[0]
    my = minMax[1]

    for row in range(min(a[1] - my, b[1] - my), max(a[1] - my, b[1] - my)):
        for col in range(min(a[0] - mx, b[0] - mx), max(a[0] - mx, b[0] - mx)):
            if grid[row][col] == ".":
                return False
    return True


def task(data: str) -> int:
    coords = parse_input(data)
    minMax = get_min_max(coords)
    grid = get_grid(coords, minMax)

    find_perimeter(grid)
    fill(grid)
    # print_grid(grid)

    max = 0
    for i in range(len(coords)):
        a = coords[i]
        for j in range(len(coords)):
            b = coords[j]
            if a == b:
                continue

            x = abs(a[0] - b[0]) + 1
            y = abs(a[1] - b[1]) + 1
            area = x * y

            if check_allowed(grid, a, b, minMax) and area > max:
                max = area

    return max


def test_example() -> None:
    assert task(read_file("day_9/test.txt")) == 24


def test_real() -> None:
    result = task(get_data(day=9, year=2025))
    print(result)
    # assert result == 4733727792
