import sys
import functools
import operator


SUFFIX = [17, 31, 73, 47, 23]


def read_lengths(filename):
    with open(filename, 'rb') as f:
        content = f.read()

    return content.strip() + bytes(SUFFIX)


def build_hash(lengths, rounds=64):
    marks = list(range(256))
    index = 0
    skip = 0
    for _ in range(rounds):
        for length in lengths:
            twist(marks, index, length)
            index += length + skip
            index %= len(marks)
            skip += 1
    return marks


def reduce_hash(sparse_hash):
    dense_hash = []
    for b in range(0, 256, 16):
        block = sparse_hash[b:b + 16]
        compressed_block = functools.reduce(operator.xor, block)
        dense_hash.append(compressed_block)
    return dense_hash


def get_hex(dense_hash):
    return ''.join('{:02x}'.format(b) for b in dense_hash)


def twist(marks, index, length):
    # construct the list of marks to reverse
    end = index + length
    mod_end = end % len(marks)
    segment = marks[index:end]
    if mod_end != end:
        segment += marks[:mod_end]

    # reverse the list
    segment = list(reversed(segment))

    # put it back in the list of marks
    for mark in segment:
        marks[index] = mark
        index = (index + 1) % len(marks)


def main(filename, rounds=64):
    lengths = read_lengths(filename)
    sparse_hash = build_hash(lengths, rounds=rounds)
    dense_hash = reduce_hash(sparse_hash)
    hex_hash = get_hex(dense_hash)
    print(hex_hash)


if __name__ == '__main__':
    main(*sys.argv[1:])
