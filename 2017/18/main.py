# -*- coding: utf-8 -*-
import queue
import collections
import itertools


class RcvException(Exception):
    def __init__(self, registers):
        self.registers = registers

    def __str__(self):
        freq = self.registers['hz']
        lineno = self.registers['ip']
        return 'RcvException: hz={} on line {}'.format(freq, lineno)


def instruction(symbol):
    def _instruction(f):
        def execute_instruction(*args, **kwargs):
            result = f(*args, **kwargs)
            return 1 if result is None else result
        execute_instruction.symbol = symbol
        return execute_instruction
    return _instruction


class Process:

    def __init__(self, instructions):
        self.memory = instructions
        self.registers = collections.defaultdict(int)
        self.instruction_set = self.get_instruction_set()

    @classmethod
    def get_instruction_set(cls):
        instructions = {}
        for name in dir(cls):
            attr, symbol = cls._get_symbol_info(name)
            if symbol:
                instructions[symbol] = attr
        return instructions

    @classmethod
    def _get_symbol_info(cls, attrname):
        attr = getattr(cls, attrname)
        symbol = getattr(attr, 'symbol', None)
        return attr, symbol

    @property
    def ip(self):
        return self.registers['ip']

    @ip.setter
    def ip(self, value):
        self.registers['ip'] = value

    def tick(self):
        if self.ip > len(self.memory):
            raise StopIteration('')
        instruction = self.memory[self.ip]
        func, args = self.decode(instruction)
        self.ip += func(self, *args)

    def decode(self, instruction):
        name, *args = instruction.split()
        func = self.instruction_set[name]
        return func, args

    def get_value_of(self, arg):
        try:
            return int(arg)
        except ValueError:
            return self.registers[arg]

    @instruction('set')
    def _set(self, x, y):
        self.registers[x] = self.get_value_of(y)

    @instruction('add')
    def _add(self, x, y):
        self.registers[x] += self.get_value_of(y)

    @instruction('mul')
    def _mul(self, x, y):
        self.registers[x] *= self.get_value_of(y)

    @instruction('mod')
    def _mod(self, x, y):
        self.registers[x] %= self.get_value_of(y)

    @instruction('jgz')
    def _jgz(self, x, y):
        if self.get_value_of(x) > 0:
            return self.get_value_of(y)


class Mark1(Process):
    @instruction('snd')
    def _snd(self, x):
        self.registers['hz'] = self.get_value_of(x)

    @instruction('rcv')
    def _rcv(self, x):
        raise RcvException(self.registers)


class Mark2(Process):
    _next_id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registers['p'] = self._assign_id()
        self.outq = queue.Queue()
        self.inq = queue.Queue()
        self.send_count = 0

    @classmethod
    def _assign_id(cls):
        id_ = cls._next_id
        cls._next_id += 1
        return id_

    @instruction('snd')
    def _snd(self, x):
        value = self.get_value_of(x)
        self.outq.put(value)
        self.send_count += 1

    @instruction('rcv')
    def _rcv(self, x):
        try:
            self.registers['x'] = self.inq.get_nowait()
        except queue.Empty:
            return 0


class Processor:
    def __init__(self, *processes):
        self.processes = processes

    def execute(self):
        for p in itertools.cycle([self.processes]):
            p.tick()


def part_1(input_):
    instructions = input_.split('\n')
    process = Mark1(instructions)
    processor = Processor(process)
    try:
        processor.execute()
    except RcvException as e:
        hz = e.registers['hz']
        print(hz)


def part_2(input_):
    instructions = input_.split('\n')
    p1 = Mark2(instructions)
    p2 = Mark2(instructions)
    p1.inq = p2.outq
    p2.inq = p1.outq
    processor = Processor(p1, p2)
    processor.execute()
