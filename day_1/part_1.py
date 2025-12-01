from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [(line[0], int(line[1:])) for line in data.split("\n")]


def task(data: str) -> int:
    steps = parse_input(data)

    count = 0
    position = 50
    for direction, amount in steps:
        if direction == "L":
            position = (position - amount) % 100
        else:
            position = (position + amount) % 100

        if position == 0:
            count += 1

    return count


def test_example() -> None:
    assert task(read_file("day_1/test.txt")) == 3


def test_real() -> None:
    result = task(get_data(day=1, year=2025))
    print(result)
    assert result == 1177
