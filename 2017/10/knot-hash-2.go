package main

import "bytes"
import "fmt"
import "io/ioutil"
import "os"


var SUFFIX = []byte{17, 31, 73, 47, 23}


type node struct {
    Value byte
    Next *node
}

type Stack struct {
    Top *node
}

func (s *Stack) Push(value byte) {
    node := &node{Value: value, Next: s.Top}
    s.Top = node
}

func (s *Stack) Pop() byte {
    node := s.Top
    s.Top = s.Top.Next
    return node.Value
}


func readLengths(filename string) []byte {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }
    return append(bytes.TrimSpace(data), SUFFIX...)
}


func buildSparseHash(lengths []byte, numRounds int) [256]byte {
    var marks [256]byte
    for i := 0; i < 256; i += 1 {
        marks[i] = byte(i)
    }
    var index byte
    var skip int
    for r := 0; r < numRounds; r += 1 {
        for _, length := range lengths {
            twist(&marks, index, length)
            index += byte(int(length) + skip)
            skip += 1
        }
    }
    return marks
}


func twist(marks *[256]byte, index byte, length byte) {
    var segment Stack
    var i byte
    for i = 0; i < length; i += 1 {
        segment.Push(marks[index + i])
    }
    for i = 0; i < length; i += 1 {
        marks[index + i] = segment.Pop()
    }
}


func reduceHash(sparseHash [256]byte) (denseHash []byte) {
    var value byte
    for i := 0; i < 256; i += 1 {
        value ^= sparseHash[i]
        if (i + 1) % 16 == 0 {
            denseHash = append(denseHash, value)
            value = 0
        }
    }
    return
}


func toHexString(hash []byte) (hexString string) {
    for _, b := range hash {
        hexString += fmt.Sprintf("%02x", b)
    }
    return
}


func main() {
    filename := os.Args[1]
    lengths := readLengths(filename)
    sparseHash := buildSparseHash(lengths, 64)
    denseHash := reduceHash(sparseHash)
    fmt.Println(toHexString(denseHash))
}
