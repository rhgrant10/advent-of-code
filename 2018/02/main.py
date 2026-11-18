# -*- coding: utf-8 -*-
import collections
import sys


def contains(x):
    def _contains(value):
        letters = collections.Counter(value)
        return x in letters.values()
    return _contains


def pairwise(n):
    a = iter(n)
    b = iter(n)
    next(b)
    for i, j in zip(a, b):
        yield i, j


def get_hamming_distance(a, b):
    return sum(i != j for i, j in zip(a, b))


def part_1(input_):
    box_ids = input_.split('\n')
    has_two = list(filter(contains(2), box_ids))
    has_three = list(filter(contains(3), box_ids))
    return len(has_two) * len(has_three)


def part_2(input_):
    box_ids = input_.split('\n')
    box_ids.sort()
    for a, b in pairwise(box_ids):
        if get_hamming_distance(a, b) == 1:
            return ''.join(a for a, b in zip(a, b) if a == b)


def main(filename):
    with open(filename) as f:
        input_ = f.read().strip()
    print('part 1:', part_1(input_))
    print('part 2:', part_2(input_))


if __name__ == '__main__':
    main(sys.argv[1])
