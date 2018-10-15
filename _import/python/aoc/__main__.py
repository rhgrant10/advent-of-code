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
    problem = utils.get_problem(day, part)
    input_ = input_ or aocd.get_data(year=year, day=day)
    return problem(input_)


def run_one(args):
    answer = get_answer(args.year, args.day, args.part, input_=args.input)
    print(answer)


def run_all(args):
    for year in range(2017, 2018):
        for day in range(1, 25):
            for part in (1, 2):
                try:
                    answer = get_answer(year, day, part)
                except Exception as e:
                    answer = f'Exception! {e}'
                print(f'{year} day {day}, part {part}: {answer}')


if __name__ == '__main__':
    main()
