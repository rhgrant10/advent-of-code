# -*- coding: utf-8 -*-


def redistribute(banks):
    blocks = max(banks)
    index = banks.index(blocks)

    banks = list(banks)
    banks[index] = 0
    for i in range(blocks):
        index = (index + 1) % len(banks)
        banks[index] += 1

    return tuple(banks)


def count_redistribution_cycles(banks):
    seen = set()
    count = 0

    while banks not in seen:
        seen.add(banks)
        banks = redistribute(banks)
        count += 1

    return count


def count_loop_size(banks):
    seen = set()

    while banks not in seen:
        seen.add(banks)
        banks = redistribute(banks)

    count = 1
    target = banks
    banks = redistribute(banks)
    while banks != target:
        banks = redistribute(banks)
        count += 1

    return count


def read_banks(input_):
    return tuple(int(bank) for bank in input_.split())


def part_1(input_):
    banks = read_banks(input_)
    return count_redistribution_cycles(banks)


def part_2(input_):
    banks = read_banks(input_)
    return count_loop_size(banks)
