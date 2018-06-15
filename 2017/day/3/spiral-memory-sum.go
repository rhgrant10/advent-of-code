package main

import "fmt"
import "os"
import "strconv"


var LEFT = [2]int{-1, 0}
var RIGHT = [2]int{1, 0}
var UP = [2]int{0, 1}
var DOWN = [2]int{0, -1}

var UP_LEFT = [2]int{-1, 1}
var UP_RIGHT = [2]int{1, 1}
var DOWN_LEFT = [2]int{-1, -1}
var DOWN_RIGHT = [2]int{1, -1}

var CARDINALS = [4][2]int{RIGHT, UP, LEFT, DOWN}
var DIAGNOALS = [4][2]int{UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT}

var ADJACENTS = [8][2]int{RIGHT, UP, LEFT, DOWN, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT}



func move(point [2]int, offset [2]int) [2]int {
    return [2]int{point[0] + offset[0], point[1] + offset[1]}
}


func getNeighborSum(point [2]int, values map[[2]int]int) int {
    sum := 0
    for _, offset := range ADJACENTS {
        sum += values[move(point, offset)]
    }
    return sum
}


func getFirstValueGreaterThan(target int) int {
    length := 1
    point := [2]int{0, 0}
    adjustment := false

    values := make(map[[2]int]int)
    values[[2]int{0, 0}] = 1

    for {
        for _, direction := range CARDINALS {
            for i := 0; i < length; i++ {
                point = move(point, direction)
                values[point] = getNeighborSum(point, values)
                if values[point] > target {
                    return values[point]
                }
            }

            if adjustment {
                length += 1
            }
            adjustment = !adjustment
        }
    }
}


func main() {
    target, err := strconv.Atoi(os.Args[1])
    if err != nil || target < 1 {
        fmt.Print("That's not a positive integer... " + os.Args[1])
    } else {
        fmt.Print(getFirstValueGreaterThan(target))
    }
}
