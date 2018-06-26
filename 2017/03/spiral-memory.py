# -*- coding: utf-8 -*-
import math
import sys


def calculate_spiral_manhattan(square):
    if square == 1:
        return 0

    square_floor = int(math.sqrt(square - 1))
    ring_max_root = square_floor + (square_floor % 2) + 1
    ring_max = ring_max_root ** 2
    ring_id = (ring_max_root + 1) // 2 - 1

    ring_size = ring_max - (math.sqrt(ring_max) - 2) ** 2
    edge_index = ring_size - (ring_max - square)
    perpendicular = abs(edge_index % (ring_id * 2) - ring_id)

    distance = ring_id + perpendicular
    return int(distance)


def main(square):
    distance = calculate_spiral_manhattan(square)
    print(distance)


if __name__ == '__main__':
    main(sys.argv[1])
