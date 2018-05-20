// spiral-memory
package main

import "errors"
import "fmt"
import "math"


func get_problems() map[int]int {
    problems := make(map[int]int)
    problems[1] = 0
    problems[12] = 3
    problems[23] = 2
    problems[1024] = 31
    problems[347991] = -1
    return problems
}


/*
We can do this in constant time. The strategy here is to calculate
each axis of movement and sum them together. Note that the term "ring"
here is used to represent a set of squares labeled from N + 1 -> M,
where N and M are numerical squares odd consecutive odd numbers. For
example, using odds 5 and 7 we have N=25 and M=49 and which correspond
to squares 26 though 49.
*/
func calculateSpiralManhattan(square int) (int, error) {
    /*
    This approach does not work for the trivial case of square 1, so we
    handle that separately up front.
    */
    if square <= 0 {
        return 0, errors.New("Invalid number, must be greater than 0")
    } else if square == 1 {
        return 0, nil
    }

    /*
    The first axis of movement is simple because it amounts to sequentially
    counting the rings. We first note that the maximum value in each ring
    is the square of an odd number:

        ring  | max  | sqrt
        ------|------|-----
        1     | 1    | 1
        2     | 9    | 3
        3     | 25   | 5
        4     | 49   | 7
        ...   | ...  | ...

    We then use the the linear relationship (n - 1) / 2 to number the rings
    starting at 0:

        sqrt  | id
        ------|---
         1    | 0
         3    | 1
         5    | 2
         7    | 3
         ...  | ...

    The resulting ring ID is the distance along one axis needed to reach any
    square on that ring.
    */
    squareFloor := int(math.Sqrt(float64(square - 1)))
    ringMaxRoot := squareFloor + (squareFloor % 2) + 1
    ringMax := int(math.Pow(float64(ringMaxRoot), 2))
    ringId := (ringMaxRoot + 1) / 2 - 1

    /*
    The perpendicular axis is a little more difficult. To find it we find
    the number of squares along each edge of the ring. Ring 3, for example,
    which contains squares 26 - 49, has 24 squares. Each of its 4 sides would
    have 6 squares numbered 0 to 5. We call this the edge index.

    The absolute value of the difference between the ring ID and the edge index
    is the remaining perpendicular distance to the target square.
    */
    ringSize := ringMax - int(math.Pow(math.Sqrt(float64(ringMax)) - 2, 2))
    edgeIndex := ringSize - (ringMax - square)
    perpendicular := int(math.Abs(float64(edgeIndex % (ringId * 2) - ringId)))

    // Manhattan distance is sum of axis movements
    distance := ringId + perpendicular
    return distance, nil
}


func main() {
    problems := get_problems()
    for square, answer := range problems {
        fmt.Println("square: ", square)

        distance, err := calculateSpiralManhattan(square)
        if err != nil {
            fmt.Println(err)
            continue
        }

        fmt.Println("distance: ", distance)
        if distance == answer {
            fmt.Println("Correct!")
        } else if answer >= 0 {
            fmt.Println("Incorrect :(")
        }
        fmt.Println()
    }
}
