# -*- coding: utf-8 -*-
import collections
import operator


OPERATORS = {
    'inc': operator.add,
    'dec': operator.sub,
}

COMPARATORS = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}


def read_instructions(input_):
    return input_.splitlines()


def parse_instruction(line):
    operation, condition = line.split(' if ')
    perform_operation = parse_operation(operation)
    condition = parse_condition(condition)
    return perform_operation, condition


def parse_operation(operation):
    register, symbol, operand = operation.split()
    operand = int(operand)

    def perform_operation(registers):
        registers[register] = OPERATORS[symbol](registers[register], operand)

    return perform_operation


def parse_condition(condition):
    register, symbol, operand = condition.split()
    operand = int(operand)

    def compare(registers):
        return COMPARATORS[symbol](registers[register], operand)

    return compare


def execute(instructions, registers=None):
    if registers is None:
        registers = collections.defaultdict(int)
    for line in instructions:
        perform_operation, condition = parse_instruction(line)
        if condition(registers):
            perform_operation(registers)
        yield max(registers.values())


def part_1(input_):
    instructions = read_instructions(input_)
    max_values = list(execute(instructions))
    return max_values[-1]


def part_2(input_):
    instructions = read_instructions(input_)
    max_values = list(execute(instructions))
    return max(max_values)
