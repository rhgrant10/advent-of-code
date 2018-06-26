# -*- coding: utf-8 -*-
import sys
import collections


def parse_graph(filename):
    with open(filename) as f:
        data = f.read().strip()

    graph = collections.defaultdict(set)
    for line in data.splitlines():
        node, children = parse_line(line)
        graph[node] |= set(children)
    return graph


def parse_line(line):
    node, children = line.split('<->')
    children = children.split(',')
    return int(node), [int(c) for c in children]


def traverse(graph, start=0):
    seen = set()
    stack = [start]

    while stack:
        node = stack.pop()
        seen.add(node)
        stack.extend(graph[node] - seen)

    return seen


def main(filename):
    graph = parse_graph(filename)
    nodes = traverse(graph)
    print(len(nodes))


if __name__ == '__main__':
    main(sys.argv[1])
