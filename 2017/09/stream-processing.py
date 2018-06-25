import sys


class StateError(Exception):
    def __init__(self, transition, char):
        super().__init__(f'found {repr(char)} in {transition}')


def read_input_file(filename):
    with open(filename) as f:
        content = f.read().strip()
    return iter(content)


class State:
    def __init__(self, stream):
        self.stream = iter(stream)
        self.scores = []
        self.level = 0


def get_scores(stream):
    state = State(stream)
    transition = start(state)
    while transition:
        transition = transition(state)
    return state.scores


def start(state):
    char = next(state.stream)
    if char == '{':
        return new_group
    raise StateError('start', char)


def new_group(state):
    state.level += 1
    state.scores.append(state.level)
    char = next(state.stream)
    if char == '{':
        return new_group
    elif char == '<':
        return garbage
    elif char == '}':
        return end_group
    raise StateError('group', char)


def garbage(state):
    char = next(state.stream)
    if char == '!':
        return ignore
    elif char == '>':
        return end_garbage
    return garbage


def ignore(state):
    next(state.stream)
    return garbage


def end_garbage(state):
    char = next(state.stream)
    if char == ',':
        return next_group
    elif char == '}':
        return end_group
    raise StateError('end_garbage', char)


def next_group(state):
    char = next(state.stream)
    if char == '{':
        return new_group
    elif char == '<':
        return garbage
    raise StateError('next_group', char)


def end_group(state):
    state.level -= 1
    try:
        char = next(state.stream)
    except StopIteration:
        return None

    if char == '{':
        return new_group
    elif char == ',':
        return next_group
    elif char == '}':
        return end_group

    raise StateError('end_group', char)


def main(filename):
    stream = read_input_file(filename)
    scores = get_scores(stream)
    print(sum(scores))


if __name__ == '__main__':
    main(sys.argv[1])
