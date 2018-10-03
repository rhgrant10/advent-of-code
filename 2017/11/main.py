# -*- coding: utf-8 -*-


CENTER = 0, 0, 0
DIRECTIONS = {
    'n'  : ( 0,  1, -1),  # noqa
    's'  : ( 0, -1,  1),  # noqa
    'ne' : ( 1,  0, -1),  # noqa
    'sw' : (-1,  0,  1),  # noqa
    'nw' : (-1,  1,  0),  # noqa
    'se' : ( 1, -1,  0),  # noqa
}


def read_directions(input_):
    return input_.strip().split(',')


def move(point, offset):
    return tuple(sum(a) for a in zip(point, offset))


def follow(directions, start=CENTER):
    coords = [start]
    for direction in directions:
        coord = move(coords[-1], DIRECTIONS[direction])
        coords.append(coord)
    return coords


def get_destination(directions, start=CENTER):
    return follow(directions, start)[-1]


def get_distance(end, start=CENTER):
    return max(sum((a, -b)) for a, b in zip(start, end))


def part_1(input_):
    directions = read_directions(input_)
    location = get_destination(directions)
    return get_distance(location)


def part_2(input_):
    directions = read_directions(input_)
    locations = follow(directions)
    return max(get_distance(location) for location in locations)
