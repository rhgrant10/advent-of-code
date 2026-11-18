# -*- coding: utf-8 -*-
import sys


def parse_dimensions(input_):
    dimensions = input_.split('\n')
    return [tuple(map(int, d.split('x'))) for d in dimensions]


def area_required(dimensions):
    x, y, z = dimensions
    sides = x*y, x*z, y*z
    return 2 * sum(sides) + min(sides)


def length_required(dimensions):
    x, y, z = sorted(dimensions)
    return 2 * (x + y) + x * y * z


def part_1(input_):
    dimensions_list = parse_dimensions(input_)
    return sum(area_required(d) for d in dimensions_list)


def part_2(input_):
    dimensions_list = parse_dimensions(input_)
    return sum(length_required(d) for d in dimensions_list)


def main(filename):
    with open(filename) as f:
        input_ = f.read().strip()
    print('part 1:', part_1(input_))
    print('part 2:', part_2(input_))


if __name__ == '__main__':
    main(sys.argv[1])
