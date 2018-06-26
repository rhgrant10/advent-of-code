# -*- coding: utf-8 -*-
import sys


def is_valid(passphrase):
    words = passphrase.split()
    return len(set(words)) == len(words)


def main(filename):
    with open(filename) as f:
        passphrases = f.read().strip().splitlines()

    print(sum(is_valid(p) for p in passphrases))


if __name__ == '__main__':
    main(sys.argv[1])
