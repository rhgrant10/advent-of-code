# -*- coding: utf-8 -*-
import collections


class Claim:
    def __init__(self, num, x, y, w, h):
        self.num = num
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @classmethod
    def from_line(cls, line):
        id_, _, xy, hw = line.split()
        num = int(id_[1:])
        x, y = map(int, xy[:-1].split(','))
        w, h = map(int, hw.split('x'))
        return cls(num, x, y, w, h)

    def __iter__(self):
        return self.squares

    def __str__(self):
        return '#{num} @ {x},{y}: {h}x{w}'.format(**vars(self))

    @property
    def squares(self):
        for y in range(self.y, self.y + self.h):
            for x in range(self.x, self.x + self.w):
                yield x, y


def part_1(input_):
    lines = input_.strip().split('\n')
    claims = [Claim.from_line(line) for line in lines]

    registry = collections.Counter()
    for claim in claims:
        registry.update(claim)

    return sum([c > 1 for c in registry.values()])


def part_2(input_):
    lines = input_.strip().split('\n')
    claims = [Claim.from_line(line) for line in lines]

    registry = collections.defaultdict(list)
    for claim in claims:
        for square in claim:
            registry[square].append(claim)

    for square, claims in registry.items():
        try:
            claim, = claims
        except ValueError:
            continue

        if all(len(registry[sq]) == 1 for sq in claim):
            return claim.num

    raise Exception('every claim overlaps at least one other claim')
