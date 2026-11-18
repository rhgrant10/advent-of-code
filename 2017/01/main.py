# -*- coding: utf-8 -*-


def perform(sequence, get_ahead):
    ahead = get_ahead(sequence)
    total = 0
    for a, b in zip(sequence, sequence[ahead:] + sequence[:ahead]):
        if a == b:
            total += int(a)
    return total


def by_one(sequence):
    return 1


def by_half(sequence):
    return len(sequence) // 2


def part_1(input_):
    return perform(input_, get_ahead=by_one)


def part_2(input_):
    return perform(input_, get_ahead=by_half)
