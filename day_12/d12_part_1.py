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


def check_position(p: int, s: int, r: int, region: Region, shapes: list[Shape]) -> bool:
    # all the tiles are placed we have a solution (may need to be after placement?)
    if sum(region.needed.values()) == 0:
        return True

    # if reached the end return fail
    width = len(region.grid[0])
    height = len(region.grid)
    if p >= width * height:
        return False

    # skip if initial or already placed
    col = p % width
    row = p // width
    if p >= 0 and s >= 0 and region.grid[row][col] == 0:
        toPlace = shapes[s].grid

        # rotate
        for _ in range(r):
            toPlace = [
                [toPlace[len(toPlace) - 1 - j][i] for j in range(len(toPlace))]
                for i in range(len(toPlace[0]))
            ]

        # check then if ok first pass, then if second pass reached place
        for place in [False, True]:
            for r in range(len(toPlace)):
                for c in range(len(toPlace[0])):
                    nr = row + r
                    nc = col + c

                    # if out of bounds fail
                    if nr < 0 or nr >= height or nc < 0 or nc >= width:
                        # return 0 to prune branch if placement fails?
                        return False

                    if toPlace[r][c] > 0:
                        # if something already at this point fail
                        if region.grid[nr][nc] > 0:
                            # return 0 to prune branch if placement fails?
                            return False

                        if place:
                            region.grid[nr][nc] = s

        # mark a shape as placed by decrementing needed
        region.needed[s] -= 1

    # spawn the next tests
    p += 1
    for n in region.needed:
        if region.needed[n] > 0:
            for rot in range(4):
                result = check_position(p, n, rot, copy.deepcopy(region), shapes)
                if result:
                    return result

    # skip cell
    result = check_position(p, -1, -1, region, shapes)
    return result


def task(data: str) -> int:
    (shapes, regions) = parse_input(data)

    result = 0
    for r in regions:
        if check_position(-1, -1, -1, r, shapes):
            result += 1

    return result


def test_example() -> None:
    assert task(read_file("day_12/test.txt")) == 2


def test_real() -> None:
    result = task(get_data(day=1, year=2025))
    print(result)
    # assert result == 0
