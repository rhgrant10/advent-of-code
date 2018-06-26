# -*- coding: utf-8 -*-
import sys


def perform(sequence):
    half = len(sequence) // 2
    total = 0
    for a, b in zip(sequence, sequence[half:] + sequence[:half]):
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
