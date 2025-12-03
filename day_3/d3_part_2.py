from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [[int(x) for x in c] for c in data.split("\n")]


def find_best_position(ptr, pos, data):
    if pos <= 0:
        return 0

    bestValue = 0
    for i in range(ptr, -1, -1):
        value = data[i] * 10 ** (12 - pos)
        value += find_best_position(i - 1, pos - 1, data)

        if value > bestValue:
            bestValue = value

    return bestValue


def task(data: str) -> int:
    batteries = parse_input(data)

    total = 0
    for b in batteries:
        total += find_best_position(len(b) - 1, 12, b)

    return total


def test_example() -> None:
    assert task(read_file("day_3/test.txt")) == 3121910778619


def test_real() -> None:
    result = task(get_data(day=3, year=2025))
    print(result)
    assert result == 17766


# start at the end
# compute the
