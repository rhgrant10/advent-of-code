# -*- coding: utf-8 -*-
import sys


DIRECTIONS = {
    'n'  : ( 0,  1, -1),  # noqa
    's'  : ( 0, -1,  1),  # noqa
    'ne' : ( 1,  0, -1),  # noqa
    'sw' : (-1,  0,  1),  # noqa
    'nw' : (-1,  1,  0),  # noqa
    'se' : ( 1, -1,  0),  # noqa
}


def read_directions(filename):
    with open(filename) as f:
        data = f.read().strip()

    return data.split(',')


def move(point, offset):
    return tuple(sum(a) for a in zip(point, offset))


def follow(directions, start=(0, 0, 0)):
    coords = [start]
    for direction in directions:
        coord = move(coords[-1], DIRECTIONS[direction])
        coords.append(coord)
    return coords


def get_distance(start, end):
    return max(sum((a, -b)) for a, b in zip(start, end))


def main(filename):
    center = 0, 0, 0
    directions = read_directions(filename)
    locations = follow(directions, start=center)
    distances = [get_distance(location, center) for location in locations]
    print(max(distances))


if __name__ == '__main__':
    main(sys.argv[1])
