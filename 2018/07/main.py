# -*- coding: utf-8 -*-
import collections
import heapq


# "Step S must be finished before step B can begin."
def parse_instructions(text):
    requirements = collections.defaultdict(set)
    for line in text.splitlines():
        __, requirement, *__, step, __, __ = line.split()
        requirements[step].add(requirement)
        requirements[requirement] |= set()
    return requirements


def traverse(requirements):
    __, root = min((len(reqs), step) for step, reqs in requirements.items())
    queue = [root]
    seen = set(queue)
    while queue:
        step = heapq.heappop(queue)
        yield step
        for reqs in requirements.values():
            reqs -= set([step])
        for step in set(requirements) - seen:
            if not requirements[step]:
                heapq.heappush(queue, step)
                seen.add(step)


def part_1(input_):
    requirements = parse_instructions(input_)
    order = traverse(requirements)
    return ''.join(order)
