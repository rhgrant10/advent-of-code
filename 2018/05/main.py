# -*- coding: utf-8 -*-


def is_reactive(a, b):
    return a.lower() == b.lower() and a != b


def react(polymer):
    i = 1
    while i < len(polymer):
        if is_reactive(polymer[i], polymer[i - 1]):
            polymer[i - 1:i + 1] = []
            i = max(i - 1, 1)
        else:
            i += 1
    return polymer


def crispr(polymer, type_):
    return [u for u in polymer if u.lower() != type_.lower()]


def part_1(input_):
    polymer = list(input_)
    return len(react(polymer))


def part_2(input_):
    polymer = list(input_)
    types = set(unit.lower() for unit in polymer)
    results = []
    for type_ in types:
        gmo_polymer = crispr(polymer, type_)
        result = react(gmo_polymer)
        results.append(result)

    return min(len(polymer) for polymer in results)
