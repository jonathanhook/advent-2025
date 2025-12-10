from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in line.split(",")[:2]) for line in data.splitlines()]


def get_edges(coords: list) -> list:
    edges = []

    # compute the hull based on the technique you had before, but with just the points

    # do an inclusion test on each canidiate area based on if a point is either:
    # - one of the boundary points
    # - within the hull, by casting rays out in all directions and seeing if they hit an edge
    #
    # different approach could be to look for live intersections between lines in candidate and lines in hull

    return []


def task(data: str) -> int:
    coords = parse_input(data)

    return 0


def test_example() -> None:
    assert task(read_file("day_9/test.txt")) == 24


def test_real() -> None:
    result = task(get_data(day=1, year=2025))
    print(result)
    # assert result == 0
