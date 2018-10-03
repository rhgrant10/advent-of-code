# -*- coding: utf-8 -*-


def escape(maze, get_adjustment):
    index = 0
    while 0 <= index < len(maze):
        new_index = index + maze[index]
        maze[index] += get_adjustment(maze[index])
        index = new_index
        yield index


def increase(value):
    return 1


def conditionally_increase(value):
    return 1 if value < 3 else -1


def read_maze(input_):
    instructions = input_.splitlines()
    return [int(i) for i in instructions]


def count_escape_steps(maze, adjuster):
    return len(list(escape(maze, adjuster)))


def part_1(input_):
    maze = read_maze(input_)
    return count_escape_steps(maze, increase)


def part_2(input_):
    maze = read_maze(input_)
    return count_escape_steps(maze, conditionally_increase)
