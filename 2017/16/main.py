# -*- coding: utf-8 -*-
import string


MOVES = {}


def move(symbol):
    def register(f):
        MOVES[symbol] = f
        return f
    return register


@move('s')
def spin(programs, x):
    return programs[-x:] + programs[:-x]


@move('x')
def exchange(programs, a, b):
    programs[a], programs[b] = programs[b], programs[a]
    return programs


@move('p')
def partner(programs, a, b):
    i = programs.index(a)
    j = programs.index(b)
    return exchange(programs, i, j)


def parse_move(move):
    symbol = move[0]
    args = [parse_arg(v) for v in move[1:].split('/')]
    return MOVES[symbol], args


def parse_arg(text):
    if text[0] in string.digits:
        return int(text)
    return text


def dance(programs, moves):
    for move in moves:
        perform, args = parse_move(move)
        programs = perform(programs, *args)
    return programs


def part_1(input_):
    moves = input_.split(',')
    programs = list(string.ascii_lowercase[:16])
    programs = dance(programs, moves)
    return ''.join(programs)


def part_2(input_):
    moves = input_.split(',')
    original = list(string.ascii_lowercase[:16])
    programs = original.copy()
    trial = 0
    max_trials = int(1e12)
    while trial < max_trials:
        programs = dance(programs, moves)
        trial += 1
        if programs == original:
            r = max_trials % trial
            trial = max_trials - r
    return ''.join(programs)
