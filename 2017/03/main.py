# -*- coding: utf-8 -*-
import collections
from decimal import Decimal


LEFT = -1, 0
RIGHT = 1, 0
UP = 0, 1
DOWN = 0, -1

UP_LEFT = -1, 1
UP_RIGHT = 1, 1
DOWN_LEFT = -1, -1
DOWN_RIGHT = 1, -1

CARDINALS = [UP, DOWN, LEFT, RIGHT]
DIAGNOALS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def move(point, offset):
    return point[0] + offset[0], point[1] + offset[1]


def get_neighbors(point, values):
    for offset in CARDINALS + DIAGNOALS:
        yield values[move(point, offset)]


def get_manhattan_distance(square):
    if square < 1:
        raise ValueError('first square is 1')
    if square == 1:
        return 0

    # surprisingly, we have to use the Decimal class because although python
    # automatically supports arbitrarily large integers, it does not support
    # arbitrarily large floats!
    square_floor = int(Decimal.sqrt(Decimal(square) - Decimal(1)))
    ring_max_root = square_floor + (square_floor % 2) + 1
    ring_max = ring_max_root ** 2
    ring_id = (ring_max_root + 1) // 2 - 1

    # again, with the sqrts turning ints into floats - gotta use Decimal
    ring_size = ring_max - (int(Decimal(ring_max).sqrt()) - 2) ** 2
    edge_index = ring_size - (ring_max - square)
    perpendicular = abs(edge_index % (ring_id * 2) - ring_id)

    distance = ring_id + perpendicular
    return int(distance)


def get_first_value_greater_than(target):
    length = 1
    point = 0, 0
    adjustment = False
    values = collections.defaultdict(int)
    values[0, 0] = 1

    while True:
        for direction in RIGHT, UP, LEFT, DOWN:
            for i in range(length):
                point = move(point, direction)
                values[point] = value = sum(get_neighbors(point, values))
                if value > target:
                    return value

            length += int(adjustment)
            adjustment = not adjustment


def part_1(input_):
    square = int(input_)
    return get_manhattan_distance(square)


def part_2(input_):
    target = int(input_)
    return get_first_value_greater_than(target)
