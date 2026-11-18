# -*- coding: utf-8 -*-
import itertools


def parse_input(text):
    # 13 players; last marble is worth 7999 points
    num_players, __, __, __, __, __, points, __ = text.strip().split()
    return int(num_players), int(points)


def get_score(num_players, limit):
    scores = {p: 0 for p in range(num_players)}

    index = 0
    ring = [0]

    balls = range(1, limit + 1)
    players = itertools.cycle(scores)
    for ball, player in zip(balls, players):
        if ball % 23:
            index = ((index + 2) % len(ring)) or len(ring)
            ring.insert(index, ball)
        else:
            scores[player] += ball
            index = (index - 7) % len(ring)
            scores[player] += ring.pop(index)
            index %= len(ring)
    return max(scores.values())


def part_1(input_):
    num_players, points = parse_input(input_)
    score = get_score(num_players, limit=points)
    return score


def part_2(input_):
    num_players, points = parse_input(input_)
    score = get_score(num_players, limit=points * 100)
    return score
