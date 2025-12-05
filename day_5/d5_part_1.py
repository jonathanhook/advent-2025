from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> tuple[set[tuple[int, int]], list[int]]:
    inputParts = data.split("\n\n")

    fresh = set()
    for line in inputParts[0].splitlines():
        part = line.split("-")
        fresh.add((int(part[0]), int(part[1])))

    available = []
    for line in inputParts[1].splitlines():
        available.append(int(line))

    return (fresh, available)


def in_ranges(item: int, ranges: set[tuple[int, int]]) -> bool:
    for r in ranges:
        if item >= r[0] and item <= r[1]:
            return True
    return False


def task(data: str) -> int:
    fresh, available = parse_input(data)

    count = 0
    for a in available:
        if in_ranges(a, fresh):
            count += 1

    return count


def test_example() -> None:
    assert task(read_file("day_5/test.txt")) == 3


def test_real() -> None:
    result = task(get_data(day=5, year=2025))
    print(result)
    assert result == 517
