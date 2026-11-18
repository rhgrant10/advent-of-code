# -*- coding: utf-8 -*-
import collections
import functools
import operator
import sys


# Knot hash, copied from 2017/10.

NUM_ROUNDS = 64
NUM_MARKS = 256
SUFFIX = [17, 31, 73, 47, 23]


def build_hash(data, rounds=NUM_ROUNDS, append_suffix=True):
    marks = list(range(NUM_MARKS))
    skip = index = 0
    if append_suffix:
        data = data.encode('utf-8') + bytes(SUFFIX)
    for _ in range(rounds):
        for length in data:
            twist(marks, index, length)
            index += length + skip
            index %= len(marks)
            skip += 1
    return marks


def twist(marks, index, length):
    stack = []
    for i in range(length):
        stack.append(marks[(index + i) % 256])
    for i in range(length):
        marks[(index + i) % 256] = stack.pop(-1)


def reduce_hash(sparse_hash):
    dense_hash = []
    for b in range(0, 256, 16):
        block = sparse_hash[b:b + 16]
        compressed_block = functools.reduce(operator.xor, block)
        dense_hash.append(compressed_block)
    return dense_hash


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
    sparse_hash = build_hash(text)
    dense_hash = reduce_hash(sparse_hash)
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


def main(filename):
    with open(filename) as f:
        input_ = f.read().strip()
    print('part 1:', part_1(input_))
    print('part 2:', part_2(input_))


if __name__ == '__main__':
    main(sys.argv[1])
