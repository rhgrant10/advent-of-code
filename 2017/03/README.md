Spiral Memory
=============

## Part 1

We can do this in constant time<sup id="a1">[1](#f1)</sup>. The strategy here is to calculate each axis of movement and sum them together.

The term "ring" is used below to represent a set of squares labeled from `N + 1` to `M`, where `N` and `M` are the numerical squares of consecutive odd numbers. For example, using consecutive odd numbers 5 and 7 we have N=25 and M=49 and which correspond to squares 26 though 49.

Note that this approach does not work for the trivial case of square 1, so we handle that separately up front.

### First Axis

The first axis of movement is simple because it amounts to sequentially counting the rings. We first note that the maximum value in each ring is the square of an odd number:

| ring  | max   | sqrt  |
| :---: | :---: | :---: |
| 1     | 1     | 1     |
| 2     | 9     | 3     |
| 3     | 25    | 5     |
| 4     | 49    | 7     |
| ...   | ...   | ...   |

We then use the the linear relationship `(n - 1) / 2` to number the rings starting at 0:

| sqrt  | id    |
| :---: | :---: |
|  1    | 0     |
|  3    | 1     |
|  5    | 2     |
|  7    | 3     |
|  ...  | ...   |

The resulting ring ID is the distance along one axis needed to reach any square on that ring.

### Perpendicular Axis

The perpendicular axis is a little more difficult. To find it we find the number of squares along each edge of the ring. Ring 3, for example, which contains squares 26 - 49, has 24 squares. Each of its 4 sides would have 6 squares numbered 0 to 5. This value is termed the edge index.

The absolute value of the difference between the ring ID and the edge index is the remaining perpendicular distance to the target square.

### Final Step

Finally, the Manhattan distance is simply the sum of these two axis movements.

<b id="f1">1</b> Technically it's linear in relation to the number of bits in the input number.[↩](#a1)

## Part 2

Ideally we would only need to track two rings: the current one being filled in and the one just inside it. However, the approach here is more naive.

Store values by their coordinates, and as we move a "cursor" around in a square spiral we simple sum up all neighbors and fill in the current square.

This is done in linear time.
