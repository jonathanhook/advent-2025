from aocd import get_data


class Machine:
    def __init__(self, target: str, buttons: list):
        self.target = target
        self.buttons = buttons
        self.state = "." * len(self.target)


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    machines = []
    for line in data.splitlines():
        parts = line.split(" ")

        target = parts[0].replace("[", "").replace("]", "")

        buttons = []
        for b in parts[1:-1]:
            schematic = [int(x) for x in b.replace("(", "").replace(")", "").split(",")]
            buttons.append(schematic)

        machines.append(Machine(target, buttons))

    return machines


def task(data: str) -> int:
    machines = parse_input(data)

    return 0


def test_example() -> None:
    assert task(read_file("day_10/test.txt")) == 0


def test_real() -> None:
    result = task(get_data(day=10, year=2025))
    print(result)
    # assert result == 0
