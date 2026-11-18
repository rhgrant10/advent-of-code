# -*- coding: utf-8 -*-
import sys
from decimal import Decimal


def calculate_spiral_manhattan(square):
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


def read_number(filename):
    with open(filename) as f:
        data = f.read()
    return int(data)


def main(filename):
    square = read_number(filename)
    distance = calculate_spiral_manhattan(square)
    print(distance)


if __name__ == '__main__':
    main(sys.argv[1])
