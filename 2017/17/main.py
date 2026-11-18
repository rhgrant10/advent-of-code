# -*- coding: utf-8 -*-


def perform(step_count, step_size):
    buffer = [0]
    index = 0
    for i in range(1, step_count):
        index = (index + step_size + 1) % i
        buffer.insert(index, i)

    answer = (index + 1) % len(buffer)
    return buffer[answer]


def fake_perform(step_count, step_size):
    index = 0
    answer = 0
    for i in range(1, step_count):
        index = (index + step_size + 1) % i
        if index == 0:
            answer = i
    return answer


def part_1(input_):
    step = int(input_)
    return perform(2018, step)


def part_2(input_):
    step = int(input_)
    return fake_perform(50_000_000, step)
