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


def task(data: str) -> int:
    parsed = parse_input(data)

    return 0


def test_example() -> None:
    assert task(read_file("day_12/test.txt")) == 2


def test_real() -> None:
    result = task(get_data(day=1, year=2025))
    print(result)
    # assert result == 0
