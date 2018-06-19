import sys
import collections


class Node:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.total_weight = None
        self.children = []


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


def print_tree(node, indent='  ', level=0):
    print(f'{indent * level}{node.name} ({node.weight})')
    for child in node.children:
        print_tree(child, level=level + 1)


def print_real_tree(node, indent='  ', level=0):
    weight = node.weight
    for child in node.children:
        weight += print_real_tree(child, level=level + 1)
    print(f'{indent * level}{node.name} ({weight})')
    return weight


def calculate_total_weight(node):
    weights = []
    for child in node.children:
        weights.append(calculate_total_weight(child))
    node.total_weight = node.weight + sum(weights)
    return node.total_weight


def find_imbalance(node):
    for child in node.children:
        imbalance = find_imbalance(child)
        if imbalance:
            return imbalance
    for child in node.children:
        weight = get_correct_weight(child, node.children)
        if child.weight != weight:
            return weight
    return None


def get_correct_weight(node, siblings):
    weights = [s.total_weight for s in siblings]
    weights.sort()
    if weights[0] == weights[1]:
        correct_weight = weights[0]
    elif weights[-2] == weights[-1]:
        correct_weight = weights[-1]
    else:
        raise Exception('wat')

    diff = correct_weight - node.total_weight
    return node.weight + diff


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
    calculate_total_weight(node)
    print(find_imbalance(node))


if __name__ == '__main__':
    main(sys.argv[1])
