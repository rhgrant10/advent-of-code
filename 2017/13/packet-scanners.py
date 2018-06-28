# -*- coding: utf-8 -*-
import sys


def parse_firewall(filename):
    with open(filename) as f:
        scanners = f.read().splitlines()

    return [list(map(int, line.split(':'))) for line in scanners]


def cross(firewall):
    cost = 0
    for depth, range_ in firewall:
        period = 2 * (range_ - 1)
        if depth % period == 0:
            cost += depth * range_
    return cost


def main(filename):
    firewall = parse_firewall(filename)
    severity = cross(firewall)
    print(severity)


if __name__ == '__main__':
    main(sys.argv[1])
