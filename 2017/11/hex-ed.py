r"""
Use a 3d grid, like Q*bert :)

     y

     |
     |
    / \
   /   \
  /     \

z         x

   y
    \  n   /
  nw +----+ ne
    /      \
  -+        +- x
    \      /
  sw +----+ se
    /  s   \
   z

   y
    \ 0+-  /
-+0  +---+  +0-
    /     \
---+       +--- x
    \     /
-0+  +---+  +-0
    / 0-+  \
   z

"""
import sys


N = 'n'
S = 's'
NE = 'ne'
SW = 'sw'
NW = 'nw'
SE = 'se'


DIRECTIONS = {
    N  : ( 0,  1, -1),  # noqa
    S  : ( 0, -1,  1),  # noqa
    NE : ( 1,  0, -1),  # noqa
    SW : (-1,  0,  1),  # noqa
    NW : (-1,  1,  0),  # noqa
    SE : ( 1, -1,  0),  # noqa
}


def read_directions(filename):
    with open(filename) as f:
        data = f.read().strip()

    return data.split(',')


def move(point, offset):
    return tuple(sum(a) for a in zip(point, offset))


def follow(directions, start=(0, 0, 0)):
    coord = start
    for direction in directions:
        coord = move(coord, DIRECTIONS[direction])
    return coord


def get_distance(start, end):
    return max(sum((a, -b)) for a, b in zip(start, end))


def main(filename):
    center = 0, 0, 0
    directions = read_directions(filename)
    location = follow(directions, start=center)
    distance = get_distance(location, center)
    print(distance)


if __name__ == '__main__':
    main(sys.argv[1])
