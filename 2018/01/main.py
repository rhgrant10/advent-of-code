# -*- coding: utf-8 -*-


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
