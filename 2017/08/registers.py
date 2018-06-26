# -*- coding: utf-8 -*-
import sys
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


def parse_input_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


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


def execute(instructions, registers):
    for line in instructions:
        perform_operation, condition = parse_instruction(line)
        if condition(registers):
            perform_operation(registers)


def main(filename):
    instructions = parse_input_file(filename)
    registers = collections.defaultdict(int)
    execute(instructions, registers)
    print(max(registers.values()))


if __name__ == '__main__':
    main(sys.argv[1])
