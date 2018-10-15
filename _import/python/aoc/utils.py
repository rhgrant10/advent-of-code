# -*- coding: utf-8 -*-
from . import problems
from . import exceptions


class Stack(list):
    @property
    def top(self):
        return self[-1]

    def push(self, value):
        return self.append(value)

    def pop(self):
        return super().pop(-1)


def get_day(number):
    try:
        return problems.BY_DAY_NUMBER[number]
    except KeyError:
        raise exceptions.NoSuchException('day', number)


def get_part(day, part):
    try:
        return getattr(day, f'part_{part}')
    except AttributeError:
        raise exceptions.NoSuchException('part', part)


def get_problem(day, part):
    return get_part(get_day(day), part)
