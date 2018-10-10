# -*- coding: utf-8 -*-
import collections

from . import hash


UP = 0, -1
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0
NEIGHBORS = UP, DOWN, LEFT, RIGHT


def get_disk_state(key_string):
    grid = collections.defaultdict(bool)
    for y in range(128):
        row_key = f'{key_string}-{y}'
        knot_hash = get_knot_hash(row_key)
        for x, bit in enumerate(get_bin(knot_hash)):
            grid[x, y] = bit == '1'
    return grid


def get_knot_hash(text):
    sparse_hash = hash.build_hash(text)
    dense_hash = hash.reduce_hash(sparse_hash)
    return dense_hash


def get_bin(value):
    return ''.join('{:08b}'.format(b) for b in value)


def get_row_state(hash_):
    binary = get_bin(hash_)
    return [bit == '1' for bit in binary]


def count_used(grid):
    return sum(grid.values())


def count_islands(grid):
    visited = set()
    count = 0

    for coord, is_used in grid.items():
        if not is_used or coord in visited:
            continue

        count += 1
        stack = [coord]
        visited.add(coord)

        while stack:
            coord = stack.pop(-1)
            for neighbor in get_connected_neighbors(coord):
                if neighbor not in visited and grid[neighbor]:
                    stack.append(neighbor)
                visited.add(neighbor)

    return count


def get_connected_neighbors(coord):
    for offset in NEIGHBORS:
        neighbor = move(coord, offset)
        if is_inbounds(neighbor):
            yield neighbor


def move(coord, offset):
    return tuple(sum(pairs) for pairs in zip(coord, offset))


def is_inbounds(coord, size=128):
    return all(0 <= n < size for n in coord)


def part_1(input_):
    grid = get_disk_state(input_)
    return count_used(grid)


def part_2(input_):
    grid = get_disk_state(input_)
    return count_islands(grid)
