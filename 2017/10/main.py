# -*- coding: utf-8 -*-
import functools
import operator


NUM_ROUNDS = 64
NUM_MARKS = 256
SUFFIX = [17, 31, 73, 47, 23]


def read_lengths(input_):
    return [int(n) for n in input_.split(',')]


def read_data(input_):
    return input_


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


def get_hex(dense_hash):
    return ''.join('{:02x}'.format(b) for b in dense_hash)


def part_1(input_):
    lengths = read_lengths(input_)
    marks = build_hash(lengths, rounds=1, append_suffix=False)
    return marks[0] * marks[1]


def part_2(input_):
    data = read_data(input_)
    sparse_hash = build_hash(data, rounds=NUM_ROUNDS)
    dense_hash = reduce_hash(sparse_hash)
    return get_hex(dense_hash)
