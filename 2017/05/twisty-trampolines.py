# -*- coding: utf-8 -*-
import sys


def escape(maze):
    index = 0
    while 0 <= index < len(maze):
        new_index = index + maze[index]
        maze[index] += 1
        index = new_index
        yield index


def count_escape_steps(filename):
    with open(filename) as f:
        instructions = f.read().splitlines()

    maze = [int(i) for i in instructions]
    return len(list(escape(maze)))


if __name__ == '__main__':
    print(count_escape_steps(sys.argv[1])
