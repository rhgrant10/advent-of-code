# -*- coding: utf-8 -*-
import collections
import itertools


CENTER = 0, 0
DIRECTIONS = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (1, 0),
    'v': (-1, 0),
}


def parse_directions(input_):
    return [DIRECTIONS[i] for i in input_]


def translate(a, b):
    return tuple(map(sum, zip(a, b)))


def deliver(directions, santas=1):
    visited = collections.Counter()
    houses = {i: CENTER for i in range(1, santas + 1)}

    visited[CENTER] += 1
    for h, move in zip(itertools.cycle(houses), directions):
        houses[h] = translate(houses[h], move)
        visited[houses[h]] += 1

    return visited


def part_1(input_):
    directions = parse_directions(input_)
    visited = deliver(directions, santas=1)
    return len(visited)


def part_2(input_):
    directions = parse_directions(input_)
    visited = deliver(directions, santas=2)
    return len(visited)
