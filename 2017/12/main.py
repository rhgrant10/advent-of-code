# -*- coding: utf-8 -*-
import collections


def parse_graph(input_):
    graph = collections.defaultdict(set)
    for line in input_.strip().splitlines():
        node, children = parse_line(line)
        graph[node] |= set(children)
    return graph


def parse_line(line):
    node, children = line.split('<->')
    children = children.split(',')
    return int(node), [int(c) for c in children]


def count_programs_in_group(graph, group=0):
    seen = set()
    stack = [group]

    while stack:
        node = stack.pop()
        seen.add(node)
        stack.extend(graph[node] - seen)

    return len(seen)


def count_groups(graph):
    unvisited = set(graph)

    groups = []
    while unvisited:
        stack = [unvisited.pop()]
        group = set()
        while stack:
            node = stack.pop()
            group.add(node)
            stack.extend(graph[node] - group)
        groups.append(group)
        unvisited -= group

    return len(groups)


def part_1(input_):
    graph = parse_graph(input_)
    return count_programs_in_group(graph, group=0)


def part_2(input_):
    graph = parse_graph(input_)
    return count_groups(graph)
