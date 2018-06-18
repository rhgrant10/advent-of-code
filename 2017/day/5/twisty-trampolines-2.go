package main

import "fmt"
import "io/ioutil"
import "os"
import "strings"
import "strconv"


func createMaze(filename string) []int {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    instructions := strings.Trim(string(data), "\n")
    lines := strings.Split(instructions, "\n")

    var maze []int
    for _, line := range lines {
        offset, err := strconv.Atoi(line)
        if err != nil {
            panic(err)
        }
        maze = append(maze, offset)
    }

    return maze
}


func countEscapeSteps(maze []int) (steps int) {
    var index int
    for 0 <= index && index < len(maze) {
        newIndex := index + maze[index]
        if maze[index] < 3 {
            maze[index] += 1
        } else {
            maze[index] -= 1
        }
        index = newIndex
        steps += 1
    }
    return
}


func main() {
    maze := createMaze(os.Args[1])
    count := countEscapeSteps(maze)
    fmt.Println(count)
}
