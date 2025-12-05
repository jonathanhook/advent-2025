from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list[tuple[int, int]]:
    inputParts = data.split("\n\n")

    fresh = []
    for line in inputParts[0].splitlines():
        part = line.split("-")
        fresh.append((int(part[0]), int(part[1])))

    return fresh


def combine_ranges(fresh: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    while i < len(fresh) - 1:
        current = fresh[i]
        next = fresh[i + 1]

        if next[0] <= current[1]:
            if current[1] < next[1]:
                fresh[i] = (current[0], next[1])
            else:
                fresh[i] = (current[0], current[1])

            fresh.remove(next)
        else:
            i += 1

    return fresh


def task(data: str) -> int:
    fresh = parse_input(data)
    fresh.sort(key=lambda x: x[0])

    combined = combine_ranges(fresh)

    total = 0
    for c in combined:
        rangeTotal = c[1] - c[0] + 1
        total += rangeTotal

    return total


def test_example() -> None:
    assert task(read_file("day_5/test.txt")) == 14


def test_custom() -> None:
    assert task(read_file("day_5/test_custom.txt")) == 17


def test_real() -> None:
    result = task(get_data(day=5, year=2025))
    print(result)
    assert result == 336173027056994
