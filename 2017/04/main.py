# -*- coding: utf-8 -*-


def contains_duplicates(passphrase):
    words = passphrase.split()
    return len(set(words)) == len(words)


def contains_anagrams(passphrase):
    words = passphrase.split()
    return len(set(tuple(sorted(word)) for word in words)) == len(words)


def read_passphrases(input_):
    return input_.strip().splitlines()


def count_valid(passphrases, is_invalid):
    return sum(not is_invalid(p) for p in passphrases)


def part_1(input_):
    passphrases = read_passphrases(input_)
    return count_valid(passphrases, contains_duplicates)


def part_2(input_):
    passphrases = read_passphrases(input_)
    return count_valid(passphrases, contains_anagrams)
