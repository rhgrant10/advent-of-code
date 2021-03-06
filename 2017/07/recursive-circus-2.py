# -*- coding: utf-8 -*-
import sys
import collections


class Node:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.total_weight = None
        self.children = []


class Level:
    def __init__(self, node, weights=None):
        self.node = node
        self.weights = weights or []


class Stack(list):
    @property
    def top(self):
        return self[-1]

    def push(self, value):
        return self.append(value)

    def pop(self):
        return super().pop(-1)


def build_tree(name, weights, children):
    root = Node(name, weights[name])
    stack = [root]
    while stack:
        node = stack.pop(-1)
        for child in children[node.name]:
            child_node = Node(child, weights[child])
            node.children.append(child_node)
            stack.append(child_node)
    return root


def find_imbalance(root):
    stack = Stack([Level(root)])
    while stack:
        if len(stack.top.weights) < len(stack.top.node.children):
            # get next child weight if we haven't visited all children yet
            i = len(stack.top.weights)
            stack.append(Level(stack.top.node.children[i]))
        else:
            # we have visited all children; if there is a unique weight, find
            # the difference from the common weight and return the unique
            # child's adjusted weight
            common, unique = get_common_and_unique(stack.top.weights)
            if unique is not None:
                diff = common - unique
                index = stack.top.weights.index(unique)
                return stack.top.node.children[index].weight + diff

            # children are balanced, so sum weights and add to parent
            total = stack.top.node.weight + sum(stack.top.weights)
            stack.pop()
            if not stack:
                return None
            stack.top.weights.append(total)


def get_common_and_unique(weights):
    if not weights:
        return None, None
    counts = collections.Counter(weights)
    if len(counts) == 1:
        return list(counts)[0], None
    return [k for k, __ in counts.most_common()]


def parse_data(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    parents = {}
    children = {}
    weights = {}

    for line in lines:
        if '->' in line:
            node, weight, __, *child_nodes = line.split()
            child_nodes = [child.strip(',') for child in child_nodes]
        else:
            node, weight = line.split()
            child_nodes = []

        weights[node] = int(weight[1:-1])
        children[node] = child_nodes
        for child_node in child_nodes:
            parents[child_node] = node

    return weights, parents, children


def find_root(nodes, parents):
    for node in nodes:
        if node not in parents:
            return node


def main(filename):
    weights, parents, children = parse_data(filename)
    root = find_root(children, parents)

    node = build_tree(root, weights, children)
    print(find_imbalance(node))


if __name__ == '__main__':
    main(sys.argv[1])
