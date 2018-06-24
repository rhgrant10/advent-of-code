import sys

import colorama


NUM_MARKS = 256


colorama.init(autoreset=True)


def read_lengths(filename):
    with open(filename) as f:
        content = f.read()

    return [int(n) for n in content.split(',')]


def print_colored_state(marks, index=0, length=0):
    selected = set([i % len(marks) for i in range(index, index + length)])
    for i, mark in enumerate(marks):
        value = str(mark).rjust(3)
        color = colorama.Fore.RED if i in selected else ''
        print(f'{color} {value}', end='  ')
        if (i + 1) % 16 == 0:
            print()
    print('\n')


def build_hash(marks, lengths):
    index = 0
    for skip, length in enumerate(lengths):
        print(f'skip = {skip}, index = {index}, length = {length}')
        print_colored_state(marks, index, length)
        twist(marks, index, length)
        index = (index + length + skip) % len(marks)


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


def main(filename, num_marks=NUM_MARKS):
    lengths = read_lengths(filename)
    marks = list(range(int(num_marks)))
    build_hash(marks, lengths)
    print_colored_state(marks)
    print(marks[0] * marks[1])


if __name__ == '__main__':
    main(*sys.argv[1:])
