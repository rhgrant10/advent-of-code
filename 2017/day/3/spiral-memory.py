#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math


PROBLEMS = {
    1: 0,
    12: 3,
    23: 2,
    1024: 31,
    347991: -1,
}


# see sprial-memory.go for an explanation of the algorithm
def calculate_spiral_manhattan(square):
    if square <= 0:
        raise ValueError('Invalid number, must be greater than 0')
    elif square == 1:
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


def main():
    for square, answer in PROBLEMS.items():
        print('square: ', square)

        try:
            distance = calculate_spiral_manhattan(square)
        except ValueError as e:
            print(e)

        print('distance: ', distance)
        if distance == answer:
            print('Correct!')
        elif answer is not None:
            print('Incorrect :(')
        print()


if __name__ == '__main__':
    main()
