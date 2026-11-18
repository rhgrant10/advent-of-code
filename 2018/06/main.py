# -*- coding: utf-8 -*-
import collections
import itertools
import string

import colored


def parse_points(text):
    lines = text.strip().split('\n')
    for id_, line in zip(string.printable, lines):
        x, y = map(int, line.split(','))
        yield id_, (x, y)


def get_extents(coords):
    minx = maxx = miny = maxy = 0
    for x, y in coords:
        if x < minx:
            minx = x
        elif x > maxx:
            maxx = x
        if y < miny:
            miny = y
        elif y > maxy:
            maxy = y
    return minx, maxx, miny, maxy


def get_coords(minx, maxx, miny, maxy):
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            yield x, y


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def calculate_closest(start, ends, distance=manhattan):
    if not ends:
        return None
    if len(ends) == 1:
        return next(iter(ends))

    first, second, *_ = sorted((distance(start, ends[n]), n) for n in ends)
    return None if first[0] == second[0] else first[1]


def create_grid(points, extents):
    grid = collections.defaultdict(lambda: None)
    for point in get_coords(*extents):
        grid[point] = calculate_closest(point, points)
    return grid


def get_perimeter_coords(minx, maxx, miny, maxy):
    return itertools.chain(
        [(minx, y) for y in range(miny, maxy + 1)],  # left
        [(maxx, y) for y in range(miny, maxy + 1)],  # right
        [(x, miny) for x in range(minx, maxx + 1)],  # bottom
        [(x, maxy) for x in range(minx, maxx + 1)],  # top
    )


def get_edge_areas(grid, extents):
    return set(grid[xy] for xy in get_perimeter_coords(*extents))


def display(grid, extents, border=None):
    minx, maxx, miny, maxy = extents
    border = border or [colored.fore.BLACK, colored.back.INDIAN_RED_1B]

    lines = []
    for y in range(miny, maxy + 1):
        is_horizontal_edge = not (miny < y < maxy)
        line = ''
        for x in range(minx, maxx + 1):
            closest = grid[x, y] or ' '
            if is_horizontal_edge or not (minx < x < maxx):
                line += colored.stylize(closest, border)
            else:
                line += closest
        lines.append(line)

    return '\n'.join(lines)


def find_closest(coordinates, limit, start):
    closest = set()
    seen = set([start])
    queue = [start]
    while queue:
        point = queue.pop(0)
        total = sum(manhattan(point, c) for c in coordinates)
        if total <= limit:
            closest.add(point)
            unseen_neighbors = neighbors(point) - seen
            queue.extend(unseen_neighbors)
            seen.update(unseen_neighbors)
    return closest


def neighbors(point):
    x, y = point
    return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}


def find_center(points):
    xs, ys = zip(*points)
    return avg_int(xs), avg_int(ys)


def avg_int(values):
    return sum(values) // len(values)


def part_1(input_):
    points = dict(parse_points(input_))

    extents = get_extents(points.values())
    grid = create_grid(points, extents)
    # print(display(grid, extents))

    areas = collections.Counter(grid.values())
    edge_areas = get_edge_areas(grid, extents)
    finite_areas = set(areas) - edge_areas

    return max(size for area, size in areas.items() if area in finite_areas)


def part_2(input_):
    __, coordinates = zip(*list(parse_points(input_)))
    start = find_center(coordinates)
    region = find_closest(coordinates, 10000, start)
    return len(region)
