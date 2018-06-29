# -*- coding: utf-8 -*-
import sys


def parse_firewall(filename):
    with open(filename) as f:
        scanners = f.read().splitlines()

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


def main(filename):
    firewall = parse_firewall(filename)
    delay = get_min_delay(firewall)
    print(delay)


if __name__ == '__main__':
    main(sys.argv[1])
