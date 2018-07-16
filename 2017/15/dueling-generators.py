# -*- coding: utf-8 -*-
import sys


LIMIT = 2147483647
NUM_PAIRS = int(40e6)
NUM_BITS = 16

FACTOR_A = 16807
FACTOR_B = 48271


class Generator:
    def __init__(self, start, factor, limit):
        self.value = start
        self.factor = factor
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        value = self.value
        self.value = self.get_next(value)
        return value

    def get_next(self, value):
        value *= self.factor
        return value % self.limit


def have_equal_lsbs(a, b, num_bits):
    mask = 2 ** num_bits - 1
    a &= mask
    b &= mask
    return a == b


def judge(a, b, num_pairs, num_bits):
    count = 0
    for _, a, b in zip(range(num_pairs), a, b):
        if have_equal_lsbs(a, b, num_bits):
            count += 1
    return count


def main(start_a, start_b):
    gen_a = Generator(start_a, FACTOR_A, LIMIT)
    gen_b = Generator(start_b, FACTOR_B, LIMIT)
    count = judge(gen_a, gen_b, NUM_PAIRS, NUM_BITS)
    print(count)


if __name__ == '__main__':
    a, b = sys.argv[1:]
    main(int(a), int(b))
