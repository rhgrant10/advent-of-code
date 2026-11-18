# -*- coding: utf-8 -*-
import sys
import argparse

import aocd

from . import utils


def main(args=None):
    parser = argparse.ArgumentParser(description='Run an AoC problem.')
    subparsers = parser.add_subparsers()

    one_parser = subparsers.add_parser('one')
    one_parser.add_argument('year', type=int)
    one_parser.add_argument('day', type=int)
    one_parser.add_argument('part', type=int)
    one_parser.add_argument('-i', '--input', type=str, required=False)
    one_parser.set_defaults(func=run_one)

    all_parser = subparsers.add_parser('all')
    all_parser.set_defaults(func=run_all)

    args = parser.parse_args(args or sys.argv[1:])
    args.func(args)


def get_answer(year, day, part, input_=None):
    problem = utils.get_problem(year, day, part)
    input_ = input_ or aocd.get_data(year=year, day=day)
    return problem(input_)


def run_one(args):
    answer = get_answer(args.year, args.day, args.part, input_=args.input)
    print(answer)


def run_all(args):
    print('Problem  \tAnswer')
    for year, day, part, problem in sorted(utils.find_problems()):
        print(f'{year} {day:>2}.{part}', end='\t', flush=True)
        try:
            input_ = aocd.get_data(year=year, day=day)
            print(problem(input_))
        except (KeyboardInterrupt, Exception) as e:
            print(e)


if __name__ == '__main__':
    main()
