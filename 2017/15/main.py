# -*- coding: utf-8 -*-


LIMIT = 2147483647
NUM_PAIRS = int(40e6)
NUM_BITS = 16

FACTOR_A = 16807
FACTOR_B = 48271

MULTIPLE_A = 4
MULTIPLE_B = 8


def yes():
    return True


class Generator:
    def __init__(self, start, factor, limit=LIMIT, is_valid_value=yes):
        self.value = start
        self.factor = factor
        self.limit = limit
        self.is_valid = is_valid_value

    def __iter__(self):
        return self

    def __next__(self):
        value = self.get_next(self.value)
        while not self.is_valid(value):
            value = self.get_next(value)
        self.value = value
        return value

    def get_next(self, value):
        value *= self.factor
        return value % self.limit


def have_equal_lsbs(a, b, num_bits):
    mask = 2 ** num_bits - 1
    a &= mask
    b &= mask
    return a == b


def judge(a, b, num_pairs=NUM_PAIRS, num_bits=NUM_BITS):
    count = 0
    for _, a, b in zip(range(num_pairs), a, b):
        if have_equal_lsbs(a, b, num_bits):
            count += 1
    return count


def create_multiple_filter(multiple):
    def is_multiple(value):
        return value % multiple == 0


def get_generator_starts(data):
    for line in data.strip().splitlines():
        start = line.split()[-1]
        yield int(start)


def part_1(input_):
    start_a, start_b = get_generator_starts(input_)
    gen_a = Generator(start_a, FACTOR_A)
    gen_b = Generator(start_b, FACTOR_B)
    return judge(gen_a, gen_b)


def part_2(input_):
    start_a, start_b = get_generator_starts(input_)
    gen_a = Generator(start_a, FACTOR_A, create_multiple_filter(MULTIPLE_A))
    gen_b = Generator(start_b, FACTOR_B, create_multiple_filter(MULTIPLE_B))
    return judge(gen_a, gen_b)
