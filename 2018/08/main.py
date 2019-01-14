# -*- coding: utf-8 -*-
import itertools
import string


def name_generator(characters=string.ascii_uppercase):
    n = 1
    while True:
        for letters in itertools.combinations_with_replacement(characters, n):
            yield ''.join(letters)
        n += 1


_names = name_generator()


class Node:

    def __init__(self):
        self.name = next(_names)
        self.children = []
        self.metadata = []

    def __str__(self):
        return f'{self.name}={repr(self.metadata)}'


def create_tree(numbers, sibling_count=1):
    nodes = []
    for __ in range(sibling_count):
        node = Node()
        num_children = numbers.pop(0)
        metadata_count = numbers.pop(0)
        node.children = create_tree(numbers, num_children)
        for __ in range(metadata_count):
            node.metadata.append(numbers.pop(0))
        nodes.append(node)
    return nodes


def print_tree(node, level=0):
    print(' ' * level, node.name, node.metadata)
    for child in node.children:
        print_tree(child, level + 2)


def get_metadata(node):
    yield node.metadata
    for child in node.children:
        yield from get_metadata(child)


def part_1(input_):
    numbers = [int(n) for n in input_.strip().split()]
    tree, = create_tree(numbers)
    metadata = get_metadata(tree)
    return sum(itertools.chain(*metadata))
