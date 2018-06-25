package main

import "fmt"
import "io/ioutil"
import "os"
import "strings"


type Point [3]int


var DIRECTIONS = map[string]Point{
    "n" : [3]int{ 0,  1, -1},
    "s" : [3]int{ 0, -1,  1},
    "ne": [3]int{ 1,  0, -1},
    "sw": [3]int{-1,  0,  1},
    "nw": [3]int{-1,  1,  0},
    "se": [3]int{ 1, -1,  0},
}


var CENTER = [3]int{0, 0, 0}


func readDirections(filename string) []string {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    var contents = strings.TrimSpace(string(data))
    return strings.Split(contents, ",")
}


func follow(directions []string, start Point) Point {
    var coord = start
    for _, direction := range directions {
        coord = move(coord, DIRECTIONS[direction])
    }
    return coord
}


func move(point Point, offset Point) (result Point) {
    result[0] = point[0] + offset[0]
    result[1] = point[1] + offset[1]
    result[2] = point[2] + offset[2]
    return
}


func getDistance(end Point, start Point) (distance int) {
    for i := 0; i < 3; i += 1 {
        var difference = end[i] - start[i]
        if difference > distance {
            distance = difference
        }
    }
    return
}


func main() {
   var filename = os.Args[1]
   var directions = readDirections(filename)
   var location = follow(directions, CENTER)
   var distance = getDistance(location, CENTER)
   fmt.Println(distance)
}