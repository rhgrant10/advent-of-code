package main

import "fmt"
import "io/ioutil"
import "os"
import "strings"
import "strconv"


type node struct {
    Value int
    Next *node
}

type Stack struct {
    Top *node
}

func (s *Stack) Push(value int) {
    node := &node{Value: value, Next: s.Top}
    s.Top = node
}

func (s *Stack) Pop() int {
    node := s.Top
    s.Top = s.Top.Next
    return node.Value
}


func readLengths(filename string) (lengths []int) {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    content := strings.Trim(string(data), "\n")
    for _, value := range strings.Split(content, ",") {
        length, err := strconv.Atoi(value)
        if err != nil {
            panic(err)
        }
        lengths = append(lengths, length)
    }
    return
}


func buildHash(lengths []int) [256]int {
    var marks [256]int
    for i := 0; i < 256; i += 1 {
        marks[i] = i
    }
    var index int
    for skip, length := range lengths {
        twist(&marks, index, length)
        index += length + skip
        index %= len(marks)
    }
    return marks
}


func twist(marks *[256]int, index int, length int) {
    var segment Stack
    for i, j := index, 0; j < length; i, j = i + 1, j + 1 {
        segment.Push(marks[i % 256])
    }
    for i, j := index, 0; j < length; i, j = i + 1, j + 1 {
        marks[i % 256] = segment.Pop()
    }
}


func main() {
    filename := os.Args[1]
    lengths := readLengths(filename)
    marks := buildHash(lengths)
    fmt.Println(marks[0] * marks[1])
}
