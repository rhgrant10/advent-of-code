# -*- coding: utf-8 -*-
import collections
import heapq
import math
import time

import colored


# "Step S must be finished before step B can begin."
def parse_instructions(text):
    requirements = collections.defaultdict(set)
    for line in text.splitlines():
        __, requirement, *__, step, __, __ = line.split()
        requirements[step].add(requirement)
        requirements[requirement] |= set()
    return requirements


def get_available_steps(requirements):
    ordered = sorted(requirements.items(), key=lambda x: (len(x[1]), x[0]))
    for step, reqs in ordered:
        if len(reqs) > 0:
            break
        yield step


def traverse(requirements):
    root, *__ = get_available_steps(requirements)
    queue = [root]
    seen = set(queue)
    while queue:
        # do the next step; it is no longer required for any step
        current = heapq.heappop(queue)
        for dependencies in requirements.values():
            dependencies -= set([current])
        yield current

        # add all unseen steps with no outstanding requirements
        for step in set(requirements) - seen:
            if not requirements[step]:
                heapq.heappush(queue, step)
                seen.add(step)


def is_worker_available(workers):
    return not all(work for work, __ in workers)


def time_traversal(requirements, workers=1):
    root, *__ = get_available_steps(requirements)

    seconds = 0
    queue = [root]
    unseen = set(requirements) - set(queue)
    workers = [(0, None)] * workers
    show_work(seconds, workers, queue, unseen)

    while queue or unseen:
        messages = []

        # unseen –> ready queue
        for step in list(unseen):
            if not requirements[step]:
                messages.append(f'Ready for step {step}')
                heapq.heappush(queue, step)
                unseen.remove(step)

        # ready queue –> workers
        while queue and is_worker_available(workers):
            step = heapq.heappop(queue)
            work = get_duration(step, rate=10)
            heapq.heappushpop(workers, (work, step))
            messages.append(f'Starting step {step} (requires {work}s)')

        # determine how long to wait
        durations = set(work for work, __ in workers)
        wait = min(durations)
        if not wait and any(durations):
            wait = min(durations - {0})

        completed = set(step for work, step in workers if work == wait)
        messages.append(f'Waiting {wait:>3.1f}s...')

        show_work(seconds, workers, queue, unseen, messages=messages)

        for step_time in pace(wait, fps=20):
            for i, (work, step) in enumerate(workers):
                if not work:
                    continue
                remaining = max(0, work - step_time)
                if remaining == 0:
                    completed.add(step)
                    step = None
                workers[i] = remaining, step
            seconds += step_time
            show_work(seconds, workers, queue, unseen)

        for step in sorted(completed):
            messages.append(f'Completed step {step}')

        # free up dependent steps now that step is done
        for dependencies in requirements.values():
            dependencies -= completed

        show_work(seconds, workers, queue, unseen, messages=messages)

    # don't forget the work still being done
    messages = []
    work, __ = max(workers)
    if work:
        messages.append(f'Finishing up {work}s worth of work.')
    seconds += work
    show_work(seconds, workers, queue, unseen, messages=messages)

    return int(seconds)


def pace(seconds, rate=1, fps=30):
    if not seconds:
        return

    now = time.time()
    real_duration = seconds / rate
    deadline = now + real_duration
    frames = math.ceil(real_duration * fps)
    deadlines = [deadline - i * (real_duration / frames) for i in range(frames)]

    delta = seconds / frames
    for deadline in reversed(deadlines):
        yield delta
        while time.time() < deadline:
            pass


def show_work(seconds, workers, queue, unseen, messages=None, _messages=[]):
    # clear the screen
    print('\033[2J')

    # print 50 most recent messages
    _messages.extend(messages or [])
    for message in _messages[-50:]:
        print(message)

    # print total seconds
    print(f'total: {seconds:.1f}')

    # print in progress steps
    print()
    for (work, step) in workers:
        print(f'[{step or " "}]', end='  ')
    print('⬅ [', end='')

    # print items in queue waiting for a free worker
    for step in queue:
        print(colored.stylize(step, colored.fore.RED), end=' ')
    print(']  ⬅ [', end='')

    # print items not ready to start yet
    print(' '.join(sorted(unseen)), end=']')

    # print the time remaining for each worker
    print()
    for (work, step) in workers:
        if work:
            work = f'{work:>3.1f}'
            styles = [colored.back.RED, colored.fore.BLACK]
        else:
            work = '███'
            styles = [colored.fore.DARK_RED_1]
        print(colored.stylize(work, styles), end='  ')

    print(flush=True)


def get_duration(step, baseline=60, rate=10):
    duration = baseline + ord(step) - 64
    return duration / rate


def part_1(input_):
    requirements = parse_instructions(input_)
    order = traverse(requirements)
    return ''.join(order)


def part_2(input_):
    requirements = parse_instructions(input_)
    duration = time_traversal(requirements, workers=5)
    return duration
