from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [[int(x) for x in c] for c in data.split("\n")]


def find_best_position(pos, remaining):
    # method goal: find the best path of all and return it

    # check the possible path from this point onwards
    # find the one that's the biggest number and return that

    length = len(remaining)

    bestValue = 0

    start = length - 1
    end = 12 - pos - 2

    print(f"{end}:{start}")

    for i in range(length - 1, 12 - pos - 2, -1):  # 12 - pos - 2
        value = remaining[i] * 10**pos

        nextPos = pos + 1
        nextRemaining = remaining[: length - nextPos]
        value += find_best_position(nextPos, nextRemaining)

        if value > bestValue:
            bestValue = value

    return bestValue


def task(data: str) -> int:
    batteries = parse_input(data)

    num = find_best_position(0, batteries[0])

    return 0


def test_example() -> None:
    assert task(read_file("day_3/test.txt")) == 357


def test_real() -> None:
    result = task(get_data(day=3, year=2025))
    print(result)
    assert result == 17766


# start at the end
# compute the
