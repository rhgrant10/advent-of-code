import sys
import collections


LEFT = -1, 0
RIGHT = 1, 0
UP = 0, 1
DOWN = 0, -1

UP_LEFT = -1, 1
UP_RIGHT = 1, 1
DOWN_LEFT = -1, -1
DOWN_RIGHT = 1, -1

CARDINALS = [UP, DOWN, LEFT, RIGHT]
DIAGNOALS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


values = collections.defaultdict(int)
values[0, 0] = 1


def move(point, offset):
    return point[0] + offset[0], point[1] + offset[1]


def get_neighbors(point):
    for offset in CARDINALS + DIAGNOALS:
        yield values[move(point, offset)]


def get_first_value_greater_than(target):
    length = 1
    point = 0, 0
    adjustment = False

    while True:
        for direction in RIGHT, UP, LEFT, DOWN:
            for i in range(length):
                point = move(point, direction)
                values[point] = value = sum(get_neighbors(point))
                if value > target:
                    return value

            length += adjustment
            adjustment = not adjustment


if __name__ == '__main__':
    try:
        target = int(sys.argv[1])
    except ValueError:
        target = 0
    if target < 1:
        print(f"That's not a positive integer... {sys.argv[1]}")
    else:
        print(get_first_value_greater_than(target))
