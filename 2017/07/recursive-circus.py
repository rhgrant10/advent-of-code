# -*- coding: utf-8 -*-
import sys


def parse_tree(filename):
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
    weights, parents, children = parse_tree(filename)
    root = find_root(children, parents)
    return root


if __name__ == '__main__':
    print(main(sys.argv[1]))
