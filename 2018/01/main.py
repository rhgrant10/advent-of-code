# -*- coding: utf-8 -*-
import sys


def part_1(input_):
    changes = list(map(int, input_.split('\n')))
    return sum(changes)


def part_2(input_):
    changes = list(map(int, input_.split('\n')))
    freq = 0
    seen = set()
    while True:
        for c in changes:
            if freq in seen:
                return freq
            seen.add(freq)
            freq += c


def main(filename):
    with open(filename) as f:
        input_ = f.read().strip()
    print('part 1:', part_1(input_))
    print('part 2:', part_2(input_))


if __name__ == '__main__':
    main(sys.argv[1])
