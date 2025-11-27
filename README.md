# Advent of Code 2025

My attempts at Advent of Code 2025, written in ``Python``. Will I make it to the end?

## Template

Solutions use the following template to get started.

```python
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
```

## Run

This year I'm going to use ``pytest`` to run the tasks. No more commenting out in the main method for me.

The code can be run from the test runner or inline.