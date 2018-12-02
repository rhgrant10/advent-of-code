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


def _get_day(year, number):
    try:
        return problems.PROBLEMS[year][number]
    except KeyError:
        raise exceptions.NoSuchException('day', (year, number))


def _get_part(day, part):
    try:
        return getattr(day, f'part_{part}')
    except AttributeError:
        raise exceptions.NoSuchException('part', part)


def get_problem(year, number, part):
    day = _get_day(year, number)
    return _get_part(day, part)


def find_problems(years=None, days=None, parts=None):
    matching_years = set(years) if years else set(problems.PROBLEMS)
    for year in matching_years:
        matching_days = set(days) if days else set(problems.PROBLEMS[year])
        for day in matching_days:
            problem = problems.PROBLEMS[year][day]
            for part in parts or (1, 2):
                try:
                    yield year, day, part, _get_part(problem, part)
                except exceptions.NoSuchException:
                    pass
