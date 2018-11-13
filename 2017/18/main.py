# -*- coding: utf-8 -*-
import collections
import string


class RcvException(Exception):
    def __init__(self, registers):
        super().__init__(registers)
        self.registers = registers

    def __str__(self):
        return str(self.registers["hz"])


def opcode(symbol):
    def wrapper(f):
        setattr(f, 'symbol', symbol)
        return f
    return wrapper


class Computer(type):
    def __new__(cls, name, bases, dct):
        klass = super().__new__(cls, name, bases, dct)
        klass.instruction_set = {}
        for value in dct.values():
            if callable(value) and hasattr(value, 'symbol'):
                symbol = getattr(value, 'symbol')
                klass.instruction_set[symbol] = value
        return klass


class DuetMachine(metaclass=Computer):
    registers = string.ascii_lowercase

    def __init__(self):
        self.instructions = []

    def get_new_context(self, **kwargs):
        names = set(self.registers) | {'hz'}
        return Registers(names, **kwargs)

    def read(self, ip):
        return self.instructions[ip]

    def decode(self, instruction):
        opcode, *args = instruction.split()
        func = self.instruction_set[opcode]
        return func, args

    @staticmethod
    @opcode('snd')
    def op_snd(regs, x):
        regs['hz'] = regs.value_of(x)

    @staticmethod
    @opcode('set')
    def op_set(regs, x, y):
        regs[x] = regs.value_of(y)

    @staticmethod
    @opcode('add')
    def op_add(regs, x, y):
        regs[x] += regs.value_of(y)

    @staticmethod
    @opcode('mul')
    def op_mul(regs, x, y):
        regs[x] *= regs.value_of(y)

    @staticmethod
    @opcode('mod')
    def op_mod(regs, x, y):
        regs[x] %= regs.value_of(y)

    @staticmethod
    @opcode('rcv')
    def op_rcv(regs, x):
        if regs.value_of(x) != 0:
            raise RcvException(regs)

    @staticmethod
    @opcode('jgz')
    def op_jgz(regs, x, y):
        if regs.value_of(x) > 0:
            return regs.value_of(y)


class Process:
    def __init__(self, computer, input_, output, ip=0):
        self.input = input_
        self.output = output
        self.regs = computer.get_new_context(ip=ip)
        self.computer = computer

    def execute(self, queue):
        while True:
            instruction = self.computer.read(self.regs['ip'])
            func, args = self.computer.decode(instruction)
            self.regs['ip'] += func(self.regs, *args) or 1


class Registers(collections.defaultdict):
    standard_registers = ['ip']

    def __init__(self, registers, **kwargs):
        super().__init__(int)
        self.register_names = set(registers) | set(self.standard_registers)
        self.update(kwargs)

    def __getitem__(self, key):
        if key not in self.register_names:
            raise Exception('no such register {!r}'.format(key))
        return super().__getitem__(key)

    def value_of(self, x):
        try:
            return int(x)
        except ValueError:
            return self[x]
