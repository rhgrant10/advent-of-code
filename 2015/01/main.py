# -*- coding: utf-8 -*-


def get_move(c):
    return {'(': 1, ')': -1}[c]


def part_1(input_):
    return sum(get_move(c) for c in input_)


def part_2(input_):
    floor = 0
    for i, c in enumerate(input_, 1):
        floor += get_move(c)
        if floor == -1:
            return i
