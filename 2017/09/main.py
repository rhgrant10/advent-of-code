# -*- coding: utf-8 -*-
import sys


def read_input_file(input_):
    return iter(input_)


def parse(stream):
    depth = 0
    score = 0
    garbage_count = 0
    in_garbage = False
    skip = False

    for char in stream:
        if skip:
            skip = False
        elif char == '!':
            skip = True
        else:
            if in_garbage:
                in_garbage = char != '>'
                if in_garbage:
                    garbage_count += 1
            elif char == '<':
                in_garbage = True
            elif char == '{':
                depth += 1
                score += depth
            elif char == '}':
                depth -= 1
    return score, garbage_count


def part_1(input_):
    stream = read_input_file(input_)
    score, __ = parse(stream)
    return score


def part_2(input_):
    stream = read_input_file(input_)
    __, garbage_count = parse(stream)
    return garbage_count


def main(filename):
    with open(filename) as f:
        input_ = f.read().strip()
    print('part 1:', part_1(input_))
    print('part 2:', part_2(input_))


if __name__ == '__main__':
    main(sys.argv[1])
