import copy

from aocd import get_data


class Shape:
    def __init__(self, id: int, grid: list[list[int]]) -> None:
        self.id: int = id
        self.grid: list[list[int]] = grid


class Region:
    def __init__(self, x: int, y: int, needed: dict[int, int]) -> None:
        self.grid: list[list[int]] = [[0 for _ in range(y)] for _ in range(x)]
        self.needed: dict[int, int] = needed


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> tuple[list[Shape], list[Region]]:
    parts = data.split("\n\n")

    shapes = []
    for p in parts[:-1]:
        lines = p.splitlines()
        id = int(lines[0][0])
        grid = []
        for line in lines[1:]:
            grid.append([1 if c == "#" else 0 for c in line])

        shapes.append(Shape(id, grid))

    regions = []
    for p in parts[-1].splitlines():
        subparts = p.split(" ")
        dims = subparts[0].replace(":", "").split("x")
        x = int(dims[0])
        y = int(dims[1])

        needed = {}
        for i in range(len(subparts[1:])):
            needed[i] = int(subparts[i + 1])

        regions.append(Region(x, y, needed))

    return (shapes, regions)


def place(row: int, col: int, region: Region, toPlace: list[list[int]], s: int) -> None:
    for r in range(len(toPlace)):
        for c in range(len(toPlace[0])):
            nr = row + r
            nc = col + c
            if toPlace[r][c] > 0:
                region.grid[nr][nc] = s


def can_place(row: int, col: int, region: Region, toPlace: list[list[int]]) -> bool:
    width = len(region.grid[0])
    height = len(region.grid)

    for r in range(len(toPlace)):
        for c in range(len(toPlace[0])):
            nr = row + r
            nc = col + c

            if nr < 0 or nr >= height or nc < 0 or nc >= width:
                return False

            if toPlace[r][c] > 0 and region.grid[nr][nc] > 0:
                return False

    return True


def backtracking(p: int, s: int, r: int, region: Region, shapes: list[Shape]) -> bool:
    # if solution found
    if sum(region.needed.values()) == 0:
        return True

    # if run off the end of the array
    width = len(region.grid[0])
    height = len(region.grid)

    if p >= width * height:
        return False

    # try and place unless initial or skip
    col = p % width
    row = p // width
    if s != -1:
        toPlace = shapes[s].grid

        # rotate
        for _ in range(r):
            toPlace = [
                [toPlace[len(toPlace) - 1 - j][i] for j in range(len(toPlace))]
                for i in range(len(toPlace[0]))
            ]

        # if can't place return false
        if not can_place(row, col, region, toPlace):
            return False

        # otherwise place
        place(row, col, region, toPlace, s)
        region.needed[s] -= 1

    # if placement succeeded try next states
    p += 1
    for n in region.needed:
        if region.needed[n] > 0:
            for rot in range(4):
                result = backtracking(p, n, rot, region, shapes)
                if result:
                    return True

    # finally try not placing anything at this positon
    result = backtracking(p, -1, -1, region, shapes)
    if result:
        return True

    # undo placement if one happened (i.e. not a skip)
    if s != -1:
        place(row, col, region, toPlace, 0)
        region.needed[s] += 1

    return False


def task(data: str) -> int:
    (shapes, regions) = parse_input(data)
    result = backtracking(-1, -1, -1, regions[2], shapes)

    return 0


def test_example() -> None:
    assert task(read_file("day_12/test.txt")) == 2


def test_real() -> None:
    result = task(get_data(day=1, year=2025))
    print(result)
    # assert result == 0
