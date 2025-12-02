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

            length = len(asString)
            for j in range(2, length + 1):
                if length % j == 0:
                    partSize = length // j

                    invalid = True
                    first = asString[:partSize]
                    for k in range(1, j):
                        current = asString[partSize * k : partSize * (k + 1)]

                        if first != current:
                            invalid = False
                            break

                    if invalid:
                        total += i
                        break

    return total


def test_example() -> None:
    assert task(read_file("day_2/test.txt")) == 4174379265


def test_real() -> None:
    result = task(get_data(day=2, year=2025))
    print(result)
    assert result == 30962646823
