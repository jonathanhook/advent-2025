import operator

from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in line.split(",")[:2]) for line in data.splitlines()]


def line_orientation(p: tuple, q: tuple, r: tuple) -> int:
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0

    return 1 if val > 0 else 2


def lines_cross(a: tuple, b: tuple) -> bool:
    p1, q1 = a
    p2, q2 = b

    o1 = line_orientation(p1, q1, p2)
    o2 = line_orientation(p1, q1, q2)
    o3 = line_orientation(p2, q2, p1)
    o4 = line_orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        if o1 != 0 and o2 != 0 and o3 != 0 and o4 != 0:
            return True

    return False


def find_perimeter(coords: list) -> list:
    nsew = [
        (operator.eq, operator.lt),
        (operator.lt, operator.eq),
        (operator.eq, operator.gt),
        (operator.gt, operator.eq),
    ]

    direction = 0
    start = coords[0]
    pos = start
    last = start

    lines = []
    while direction < 4:
        x, y = nsew[direction]
        found = list(filter(lambda c: x(c[0], pos[0]) and y(c[1], pos[1]), coords))

        if len(found) == 1 and found[0] != last:
            line = (pos, found[0])

            if line in lines:
                break  # loop

            lines.append(line)
            last = pos
            pos = found[0]
            direction = 0

        elif len(found) > 1:
            raise Exception("looks like you need to implement more than one on a line!")

        else:
            direction += 1

    return lines


def check_inside(point: tuple, perimeter: list, coords: list) -> bool:
    if point in coords:
        return True

    ray = (point, (0, 0))
    intersections = 0
    for p in perimeter:
        if lines_cross(ray, p):
            intersections += 1

    return intersections % 2 != 0


def check_allowed(corners: list, perimeter: list) -> bool:
    toCheck = [
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[0], corners[0]),
    ]

    for t in toCheck:
        for p in perimeter:
            if lines_cross(t, p):
                return False

    return True


def task(data: str) -> int:
    coords = parse_input(data)
    lines = find_perimeter(coords)
    checked = set()

    max = 0
    for i in range(len(coords)):
        a = coords[i]
        for j in range(len(coords)):
            b = coords[j]
            if a == b or (b, a) in checked:
                continue
            checked.add((a, b))

            corners = [
                (a[0], a[1]),
                (a[0], b[1]),
                (b[0], b[1]),
                (b[0], a[1]),
            ]

            inside = True
            for c in [corners[1], corners[3]]:
                if not check_inside(c, lines, coords):
                    inside = False
                    break

            if not inside:
                continue

            x = abs(a[0] - b[0]) + 1
            y = abs(a[1] - b[1]) + 1
            area = x * y
            if check_allowed(corners, lines) and area > max:
                # if area > max:
                max = area

    return max


def test_example() -> None:
    assert task(read_file("day_9/test.txt")) == 24


def test_real() -> None:
    result = task(get_data(day=9, year=2025))
    print(result)
    # assert result == 4733727792
