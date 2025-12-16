import sys

from aocd import get_data


class Shape:
    def __init__(self, id: int, grid: list[list[int]]) -> None:
        self.id: int = id
        self.grid: list[list[int]] = grid
        self.size = count_non_zero(self.grid)


class Region:
    def __init__(self, x: int, y: int, needed: dict[int, int]) -> None:
        self.grid: list[list[int]] = [[0 for _ in range(y)] for _ in range(x)]
        self.needed: dict[int, int] = needed
        self.spaceLeft = len(self.grid) * len(self.grid[0])

    def update_space_left(self, shape: Shape, add: bool) -> None:
        self.spaceLeft = (
            self.spaceLeft + shape.size if add else self.spaceLeft - shape.size
        )


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
        x = int(dims[1])
        y = int(dims[0])

        needed = {}
        for i in range(len(subparts[1:])):
            needed[i] = int(subparts[i + 1])

        regions.append(Region(x, y, needed))

    return (shapes, regions)


def print_grid(region: Region) -> None:
    with open("day_12/debug.txt", "w") as f:
        for i in range(len(region.grid)):
            for j in range(len(region.grid[0])):
                val = region.grid[i][j]
                print(val if val != 0 else ".", end="", file=f)
            print("", file=f)


def place(row: int, col: int, region: Region, toPlace: list[list[int]], s: int) -> None:
    for r in range(len(toPlace)):
        for c in range(len(toPlace[0])):
            nr = row + r
            nc = col + c
            if toPlace[r][c] > 0:
                region.grid[nr][nc] = s + 1


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


def count_non_zero(grid: list[list[int]]) -> int:
    return sum(1 for row in grid for cell in row if cell != 0)


def abandon_path(region: Region, shapes: list[Shape]) -> bool:
    spaceNeeded = 0
    for n in region.needed:
        if region.needed[n] > 0:
            spaceNeeded += shapes[n].size * region.needed[n]

        if spaceNeeded > region.spaceLeft:
            return True

    return False


def backtracking(p: int, s: int, r: int, region: Region, shapes: list[Shape]) -> bool:
    # if solution found
    if sum(region.needed.values()) == 0:
        return True

    # check if path should be abandoned
    if abandon_path(region, shapes):
        return False

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
        region.update_space_left(shapes[s], True)
        region.needed[s] -= 1

        # print_grid(region)

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
        place(row, col, region, toPlace, -1)
        region.update_space_left(shapes[s], False)
        region.needed[s] += 1

    return False


def task(data: str) -> int:
    (shapes, regions) = parse_input(data)

    result = 0
    for r in regions:
        if backtracking(-1, -1, -1, r, shapes):
            result += 1

    return result


def test_example() -> None:
    assert task(read_file("day_12/test.txt")) == 2


def test_real() -> None:
    sys.setrecursionlimit(15000)
    result = task(get_data(day=12, year=2025))
    print(result)
    assert result == 492
