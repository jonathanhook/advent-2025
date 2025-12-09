from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in line.split(",")[:2]) for line in data.splitlines()]


def task(data: str) -> int:
    tiles = parse_input(data)

    max = 0
    for i in range(len(tiles)):
        a = tiles[i]
        for j in range(len(tiles)):
            b = tiles[j]
            if a == b:
                continue

            x = abs(a[0] - b[0]) + 1
            y = abs(a[1] - b[1]) + 1
            area = x * y

            if area > max:
                max = area

    return max


def test_example() -> None:
    assert task(read_file("day_9/test.txt")) == 50


def test_real() -> None:
    result = task(get_data(day=9, year=2025))
    print(result)
    assert result == 4733727792
