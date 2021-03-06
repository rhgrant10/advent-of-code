# -*- coding: utf-8 -*-
import sys


def perform(sequence):
    total = 0
    for a, b in zip(sequence, sequence[1:] + sequence[:1]):
        if a == b:
            total += int(a)
    return total


def parseCaptcha(filename):
    with open(filename) as f:
        return f.read().strip()


def main(filename):
    captcha = parseCaptcha(filename)
    print(perform(captcha))


if __name__ == '__main__':
    main(sys.argv[1])
