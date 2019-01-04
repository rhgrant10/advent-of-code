# -*- coding: utf-8 -*-
import collections
import functools


@functools.total_ordering
class Shift:
    def __init__(self, guard, minutes=None):
        self.guard = guard
        self.minutes = minutes or [False] * 60

    def __eq__(self, other):
        return (self.guard, self.minutes) == (other.guard, other.minutes)

    def __lt__(self, other):
        return (self.guard, self.minutes) < (other.guard, other.minutes)

    def __iter__(self):
        yield from iter(self.minutes)

    def set_sleepy(self, state, start, end=60):
        self.minutes[start:end] = [state] * (end - start)


@functools.total_ordering
class Guard:
    def __init__(self, id_, shifts=None):
        self.id = id_
        self.shifts = shifts or []

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def get_total_minutes_sleeping(self):
        return sum(sum(minutes) for minutes in self.shifts)


def get_guards(records):
    shift = None
    data = collections.defaultdict(list)
    for record in sorted(records):
        if record.endswith('begins shift'):
            if shift is not None:
                data[shift.guard].append(shift)
            guard = int(record.split()[3][1:])
            shift = Shift(guard)
        elif record.endswith('asleep'):
            minute = int(record[15:17])
            shift.set_sleepy(True, minute)
        elif record.endswith('up'):
            minute = int(record[15:17])
            shift.set_sleepy(False, minute)
        else:
            raise Exception('must start with "begins shift"')
    return [Guard(gid, shifts) for gid, shifts in data.items()]


def print_guard_records(guards):
    print('Guard Minutes')
    print('      000000000011111111112222222222333333333344444444445555555555')
    print('      012345678901234567890123456789012345678901234567890123456789')
    for guard in sorted(guards):
        for shift in sorted(guard.shifts):
            sleep_map = ''.join(['#' if minute else '.' for minute in shift])
            print('{:5} {}'.format(guard.id, sleep_map))


def part_1(input_):
    records = sorted(input_.strip().split('\n'))
    guards = get_guards(records)

    guard = max(guards, key=Guard.get_total_minutes_sleeping)
    counts = collections.Counter()
    for shift in guard.shifts:
        counts.update([i for i, s in enumerate(shift) if s])

    minute, _ = counts.most_common()[0]
    return guard.id * minute


def part_2(input_):
    records = sorted(input_.strip().split('\n'))
    guards = get_guards(records)

    times_asleep = {}
    for minute in range(60):
        for guard in guards:
            asleep = sum(shift.minutes[minute] for shift in guard.shifts)
            times_asleep[guard.id, minute] = asleep

    _, (minute, gid) = max((v, k) for k, v in times_asleep.items())
    return gid * minute


# This is what I kept thinking the problem was asking the whole time
def part_3(input_):
    records = sorted(input_.strip().split('\n'))
    guards = get_guards(records)

    chances = {}
    for minute in range(60):
        for guard in guards:
            asleep = sum(shift.minutes[minute] for shift in guard.shifts)
            chances[guard.id, minute] = asleep / len(guard.shifts)

    _, (minute, gid) = max((v, k) for k, v in chances.items())
    return gid * minute
