from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return []


def task(data: str) -> int:
    return 0


def test_example() -> None:
    assert task(read_file("test.txt")) == 0


def test_real() -> None:
    assert task(get_data(day=1, year=2025)) == 0
