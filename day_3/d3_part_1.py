from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [[int(x) for x in c] for c in data.split("\n")]


def task(data: str) -> int:
    batteries = parse_input(data)

    total = 0
    for b in batteries:
        length = len(b)
        msd = b[length - 2]
        lsd = b[length - 1]

        for i in range(length - 3, -1, -1):
            current = b[i]

            if current >= msd:
                tmp = msd
                msd = current

                if tmp >= lsd:
                    lsd = tmp

        joltage = int(f"{msd}{lsd}")
        total += joltage

    return total


def test_example() -> None:
    assert task(read_file("day_3/test.txt")) == 357


def test_real() -> None:
    result = task(get_data(day=3, year=2025))
    print(result)
    assert result == 17766
