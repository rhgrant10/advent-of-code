# -*- coding: utf-8 -*-


def parse_firewall(input_):
    scanners = input_.splitlines()
    return [list(map(int, line.split(':'))) for line in scanners]


def get_min_delay(firewall):
    delay = 0
    while is_costly(firewall, delay):
        delay += 1
    return delay


def is_costly(firewall, delay):
    for depth, range_ in firewall:
        period = 2 * (range_ - 1)
        if (depth + delay) % period == 0:
            return True
    return False


def cross(firewall):
    cost = 0
    for depth, range_ in firewall:
        period = 2 * (range_ - 1)
        if depth % period == 0:
            cost += depth * range_
    return cost


def part_1(input_):
    firewall = parse_firewall(input_)
    return cross(firewall)


def part_2(input_):
    firewall = parse_firewall(input_)
    return get_min_delay(firewall)
