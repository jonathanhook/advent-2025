import operator

import matplotlib.pyplot as plt
from aocd import get_data


def read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def parse_input(data: str) -> list:
    return [tuple(int(x) for x in line.split(",")[:2]) for line in data.splitlines()]


def draw(coords: list, lines: list, shape: list, lineColour: str) -> None:
    plt.clf()

    x_coords, y_coords = zip(*coords)
    plt.scatter(x_coords, y_coords, color="blue")

    for line in lines:
        x_line, y_line = zip(*line)
        plt.plot(x_line, y_line, color="green", linestyle="--")

    x_shape, y_shape = zip(*shape)
    plt.plot(
        x_shape + (x_shape[0],),
        y_shape + (y_shape[0],),
        color=lineColour,
        linestyle="-",
    )

    plt.show()

    return


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

        else:
            direction += 1

    return lines


def point_on_line(point: tuple, line: tuple) -> bool:
    p1, p2 = line
    if not (
        min(p1[0], p2[0]) <= point[0] <= max(p1[0], p2[0])
        and min(p1[1], p2[1]) <= point[1] <= max(p1[1], p2[1])
    ):
        return False

    if (p2[0] - p1[0]) * (point[1] - p1[1]) == (p2[1] - p1[1]) * (point[0] - p1[0]):
        return True

    return False


def point_inside(point: tuple, perimeter: list, coords: list) -> bool:
    # is on an existing point
    if point in coords:
        return True

    # is on an existing list
    for p in perimeter:
        if point_on_line(point, p):
            return True

    # otherwise raycast test
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
        print(f"checking: {i}")

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
                if not point_inside(c, lines, coords):
                    inside = False
                    break

            if not inside:
                continue

            allowed = check_allowed(corners, lines)
            if inside and allowed:
                x = abs(a[0] - b[0]) + 1
                y = abs(a[1] - b[1]) + 1
                area = x * y
                if area > max:
                    max = area

            # lineColour = "yellow" if allowed and inside else "red"
            # draw(coords, lines, corners, lineColour)

    return max


def test_example() -> None:
    assert task(read_file("day_9/test.txt")) == 24


def test_real() -> None:
    result = task(get_data(day=9, year=2025))
    print(result)
    assert result == 1566346198
