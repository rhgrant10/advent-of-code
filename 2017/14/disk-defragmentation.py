# -*- coding: utf-8 -*-
import sys
import functools
import operator


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
    return ''.join('{:016b}'.format(b) for b in dense_hash)


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


def count_used(grid):
    return sum(sum(row) for row in grid)


def main(key_string):
    grid = get_disk_state(key_string)
    num_used = count_used(grid)
    print(num_used)


if __name__ == '__main__':
    main(sys.argv[1])
