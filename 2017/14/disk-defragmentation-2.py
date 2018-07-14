# -*- coding: utf-8 -*-
import sys
import functools
import operator
import collections


SUFFIX = [17, 31, 73, 47, 23]

UP = 0, -1
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0
NEIGHBORS = UP, DOWN, LEFT, RIGHT


def build_hash(text, rounds=64):
    lengths = text.encode('utf-8') + bytes(SUFFIX)
    marks = list(range(256))
    skip = index = 0
    for _ in range(rounds):
        for length in lengths:
            twist(marks, index, length)
            index += length + skip
            index %= len(marks)
            skip += 1
    return marks


def reduce_hash(sparse_hash):
    dense_hash = []
    for b in range(0, 256, 16):
        block = sparse_hash[b:b + 16]
        compressed_block = functools.reduce(operator.xor, block)
        dense_hash.append(compressed_block)
    return dense_hash


def twist(marks, index, length):
    stack = []
    for i in range(length):
        stack.append(marks[(index + i) % 256])
    for i in range(length):
        marks[(index + i) % 256] = stack.pop(-1)


def get_bin(dense_hash):
    return ''.join('{:08b}'.format(b) for b in dense_hash)


# # #


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


def main(key_string):
    grid = get_disk_state(key_string)
    num_islands = count_islands(grid)
    print(num_islands)


if __name__ == '__main__':
    main(sys.argv[1])
