from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    parsed = [line.split() for line in data.split("\n")]

    dim = len(parsed[0])
    for entry in parsed:
        if len(entry) != dim:
            raise Exception("unexpected number of cols")

    return parsed


def task(data: str) -> int:
    parsed = parse_input(data)

    total = 0
    for i in range(0, len(parsed[0])):
        operator = ""
        subtotal = 0
        firstSet = False
        for j in range(len(parsed) - 1, -1, -1):
            if j == len(parsed) - 1:
                operator = parsed[j][i]
            elif not firstSet:
                subtotal = int(parsed[j][i])
                firstSet = True
            elif operator == "*":
                subtotal *= int(parsed[j][i])
            elif operator == "+":
                subtotal += int(parsed[j][i])
        total += subtotal

    return total


def test_example() -> None:
    assert task(read_file("day_6/test.txt")) == 4277556


def test_real() -> None:
    result = task(get_data(day=6, year=2025))
    print(result)
    assert result == 4405895212738
