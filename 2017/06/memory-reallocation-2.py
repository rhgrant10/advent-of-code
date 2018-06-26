# -*- coding: utf-8 -*-
import sys


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


def main(filename):
    with open(filename) as f:
        data = f.read()

    banks = tuple(int(bank) for bank in data.split())
    return count_redistribution_cycles(banks)


if __name__ == '__main__':
    print(main(sys.argv[1]))
