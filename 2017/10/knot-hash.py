# -*- coding: utf-8 -*-
import sys


def read_lengths(filename):
    with open(filename) as f:
        content = f.read()

    return [int(n) for n in content.split(',')]


def build_hash(marks, lengths):
    index = 0
    for skip, length in enumerate(lengths):
        twist(marks, index, length)
        index += length + skip
        index %= len(marks)


def twist(marks, index, length):
    # construct the list of marks to reverse
    end = index + length
    mod_end = end % len(marks)
    segment = marks[index:end]
    if mod_end != end:
        segment += marks[:mod_end]

    # reverse the list
    segment = list(reversed(segment))

    # put it back in the list of marks
    for mark in segment:
        marks[index] = mark
        index = (index + 1) % len(marks)


def main(filename, num_marks=256):
    lengths = read_lengths(filename)
    marks = list(range(int(num_marks)))
    build_hash(marks, lengths)
    print(marks[0] * marks[1])


if __name__ == '__main__':
    main(*sys.argv[1:])
