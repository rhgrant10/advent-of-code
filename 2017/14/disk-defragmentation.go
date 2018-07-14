package main

import "fmt"
import "os"


const NUM_KNOTS = 256
const NUM_KEYS = 128
const NUM_ROUNDS = 64


type SparseHash = [NUM_KNOTS]byte
type Coord [2]int


var SUFFIX = []byte{17, 31, 73, 47, 23}


type ByteNode struct {
    Value byte
    Next *ByteNode
}

type ByteStack struct {
    Top *ByteNode
}

func (s *ByteStack) Push(value byte) {
    node := &ByteNode{Value: value, Next: s.Top}
    s.Top = node
}

func (s *ByteStack) Pop() byte {
    node := s.Top
    s.Top = s.Top.Next
    return node.Value
}


////


func buildSparseHash(lengths []byte) SparseHash {
    var marks SparseHash
    for i := 0; i < NUM_KNOTS; i += 1 {
        marks[i] = byte(i)
    }
    var index byte
    var skip int
    for r := 0; r < NUM_ROUNDS; r += 1 {
        for _, length := range lengths {
            twist(&marks, index, length)
            index += byte(int(length) + skip)
            skip += 1
        }
    }
    return marks
}


func twist(marks *SparseHash, index byte, length byte) {
    var segment ByteStack
    var i byte
    for i = 0; i < length; i += 1 {
        segment.Push(marks[index + i])
    }
    for i = 0; i < length; i += 1 {
        marks[index + i] = segment.Pop()
    }
}


func reduceHash(sparseHash SparseHash) (denseHash []byte) {
    var value byte
    for i, knot := range sparseHash {
        value ^= knot
        if (i + 1) % 16 == 0 {
            denseHash = append(denseHash, value)
            value = 0
        }
    }
    return
}


func getKnotHash(text string) []byte {
    var lengths = append([]byte(text), SUFFIX...)
    var sparseHash = buildSparseHash(lengths)
    var denseHash = reduceHash(sparseHash)
    return denseHash
}


////


func getDiskState(keyString string) map[Coord]bool {
    var grid = make(map[Coord]bool, 0)
    for y := 0; y < NUM_KEYS; y++ {
        var rowKey = fmt.Sprintf("%s-%d", keyString, y)
        var knotHash = getKnotHash(rowKey)
        for x, bit := range getBits(knotHash) {
            var coord = Coord{x, y}
            grid[coord] = bit != 0
        }
    }
    return grid
}


func getBits(knotHash []byte) (bits []byte) {
    for _, knot := range knotHash {
        var mask byte = 1
        for i := 0; i < 8; i++ {
            var bit = knot & mask
            bits = append(bits, bit)
            mask = mask << 1
        }
    }
    return
}


func countUsed(grid map[Coord]bool) (count int) {
    for _, isUsed := range grid {
        if isUsed {
            count++
        }
    }
    return
}


func main() {
    var keyString = os.Args[1]
    var grid = getDiskState(keyString)
    var numUsed = countUsed(grid)
    fmt.Println(numUsed)
}
