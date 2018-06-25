// spiral-memory
package main

import "errors"
import "fmt"
import "math"


func getProblems() map[int]int {
    problems := make(map[int]int)
    problems[1] = 0
    problems[12] = 3
    problems[23] = 2
    problems[1024] = 31
    problems[347991] = -1
    return problems
}


func calculateSpiralManhattan(square int) (int, error) {
    if square <= 0 {
        return 0, errors.New("Invalid number, must be greater than 0")
    } else if square == 1 {
        return 0, nil
    }

    // Find the first axis.
    squareFloor := int(math.Sqrt(float64(square - 1)))
    ringMaxRoot := squareFloor + (squareFloor % 2) + 1
    ringMax := int(math.Pow(float64(ringMaxRoot), 2))
    ringId := (ringMaxRoot + 1) / 2 - 1

    // Find the perpendicular axis.
    ringSize := ringMax - int(math.Pow(math.Sqrt(float64(ringMax)) - 2, 2))
    edgeIndex := ringSize - (ringMax - square)
    perpendicular := int(math.Abs(float64(edgeIndex % (ringId * 2) - ringId)))

    // Manhattan distance is sum of axis movements
    distance := ringId + perpendicular
    return distance, nil
}


func main() {
    problems := getProblems()
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
