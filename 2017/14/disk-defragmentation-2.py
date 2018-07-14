# -*- coding: utf-8 -*-
import sys
import functools
import operator
import itertools


SUFFIX = [17, 31, 73, 47, 23]


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
    grid = []
    for i in range(128):
        row_key = f'{key_string}-{i}'
        knot_hash = get_knot_hash(row_key)
        row_state = get_row_state(knot_hash)
        grid.append(row_state)
    return grid


def get_knot_hash(text):
    sparse_hash = build_hash(text)
    dense_hash = reduce_hash(sparse_hash)
    return dense_hash


def get_row_state(hash_):
    binary = get_bin(hash_)
    return [bit == '1' for bit in binary]


def iter_squares(grid):
    for y, row in enumerate(grid):
        for x, square in enumerate(row):
            yield (y, x), square


def count_islands(grid):
    visited = set()
    count = 0

    for coord, is_used in iter_squares(grid):
        if coord in visited or not grid[coord[0]][coord[1]]:
            continue

        count += 1
        stack = [coord]
        visited.add(coord)

        while stack:
            coord = stack.pop(-1)
            for y, x in get_connected_neighbors(coord):
                coord = y, x
                if coord not in visited and grid[y][x]:
                        stack.append(coord)
                visited.add(coord)

    return count


def get_connected_neighbors(coord):
    neighborhood = get_neighborhood(coord)
    connected = [
        neighborhood[0][1],
        neighborhood[1][0], neighborhood[1][2],
        neighborhood[2][1],
    ]
    yield from [coord for coord in connected if is_inbounds(*coord)]


def get_neighborhood(coord):
    neighborhood = []
    y, x = coord
    for ny in range(y - 1, y + 2):
        street = [(ny, nx) for nx in range(x - 1, x + 2)]
        neighborhood.append(street)
    return neighborhood


def is_inbounds(y, x, size=128):
    return 0 <= x < size and 0 <= y < size


def main(key_string):
    grid = get_disk_state(key_string)
    num_islands = count_islands(grid)
    print(num_islands)


if __name__ == '__main__':
    main(sys.argv[1])
