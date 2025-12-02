from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in r.split("-")) for r in data.split(",")]


def task(data: str) -> int:
    ranges = parse_input(data)

    total = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            asString = str(i)

            if len(asString) % 2 == 0:
                midpoint = len(asString) // 2
                parts = (asString[:midpoint], asString[midpoint:])
                if parts[0] == parts[1]:
                    total += i

    return total


def test_example() -> None:
    assert task(read_file("day_2/test.txt")) == 1227775554


def test_real() -> None:
    result = task(get_data(day=2, year=2025))
    print(result)
    assert result == 24747430309
