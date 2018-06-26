package main

import "fmt"
import "os"
import "math"
import "strconv"


func calculateSpiralManhattan(square int) int {
    if square == 1 {
        return 0
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
    return distance
}


func readSquare(square string) int {
    n, err := strconv.Atoi(square)
    if err != nil {
        panic(err)
    }
    return n
}


func main() {
    var square = readSquare(os.Args[1])
    var distance = calculateSpiralManhattan(square)
    fmt.Println(distance)
}
