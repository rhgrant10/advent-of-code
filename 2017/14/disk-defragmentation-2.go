package main

import "fmt"
import "image"
import "image/color"
import "image/png"
import "math"
import "os"


// const NOT_USED = "\u2591\u2591"
const NOT_USED = "  "

const HORIZONTAL = "\u2501\u2501"
const LEFT_VERTICAL = " \u2503"
const RIGHT_VERTICAL = "\u2503"

const TOP_LEFT_CORNER = " \u250F"
const TOP_RIGHT_CORNER = "\u2513"
const BOTTOM_LEFT_CORNER = " \u2517"
const BOTTOM_RIGHT_CORNER = "\u251B"

const NUM_KNOTS = 256
const NUM_KEYS = 128
const NUM_ROUNDS = 64


type SparseHash = [NUM_KNOTS]byte
type Coord [2]int


var UP = Coord{0, -1}
var DOWN = Coord{0, 1}
var LEFT = Coord{-1, 0}
var RIGHT = Coord{1, 0}
var NEIGHBORS = [4]Coord{UP, DOWN, LEFT, RIGHT}

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


type CoordNode struct {
    Value Coord
    Next *CoordNode
}

type CoordStack struct {
    Top *CoordNode
    size int
}

func (s *CoordStack) Push(value Coord) {
    node := &CoordNode{Value: value, Next: s.Top}
    s.Top = node
    s.size++
}

func (s *CoordStack) Pop() Coord {
    node := s.Top
    s.Top = s.Top.Next
    s.size--
    return node.Value
}

func (s *CoordStack) IsEmpty() bool {
    return s.size == 0
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


func countIslands(grid map[Coord]bool) (int, map[Coord]int) {
    var islands = make(map[Coord]int, 0)

    var count int = 0
    for coord, isUsed := range grid {
        if !isUsed || islands[coord] > 0 {
            continue
        }

        count++
        var stack CoordStack
        stack.Push(coord)
        islands[coord] = count

        for !stack.IsEmpty() {
            coord = stack.Pop()
            for _, neighbor := range getConnectedNeighbors(coord) {
                if islands[neighbor] == 0 && grid[neighbor] {
                    stack.Push(neighbor)
                }
                islands[coord] = count
            }
        }
    }
    return count, islands
}


func printGrid(grid map[Coord]bool, start Coord, end Coord) {
    for y := start[1]; y <= end[1]; y++ {
        for x := start[0]; x <= end[0]; x++ {
            var coord = Coord{x, y}
            if isInbounds(coord) {
                if grid[coord] {
                    fmt.Print("#")
                } else {
                    fmt.Print(".")
                }
            } else {
                fmt.Print(string(rune(9608)))
            }
        }
        fmt.Println()
    }
}


func printIslands(grid map[Coord]int, start Coord, end Coord) {
    for y := start[1]; y <= end[1]; y++ {
        for x := start[0]; x <= end[0]; x++ {
            var coord = Coord{x, y}
            if isInbounds(coord) {
                var index = grid[coord]
                if index > 0 {
                    fmt.Print(printable(index))
                } else {
                    fmt.Print(NOT_USED)
                }
            } else {
                fmt.Print(outOfBoundsChar(coord))
            }
        }
        fmt.Println()
    }
}


func drawIslands(grid map[Coord]int, palette []color.Color) image.Image {
    var image = image.NewRGBA(image.Rect(0, 0, 128, 128))
    for y := 0; y <= 128; y++ {
        for x := 0; x <= 128; x++ {
            var coord = Coord{x, y}
            var colorId = grid[coord] % len(palette)
            image.Set(x, y, palette[colorId])
        }
    }
    return image
}


func convertToRGB(hue float64, saturation float64, value float64) color.NRGBA {
    var i int = int(hue * 6)
    var f float64 = hue * 6 - float64(i)
    var p float64 = value * (1 - saturation)
    var q float64 = value * (1 - f - saturation)
    var t float64 = value * (1 - (1 - f) * saturation)

    var r, g, b float64
    switch i % 6 {
        case 0: r, g, b = value, t, p
        case 1: r, g, b = q, value, p
        case 2: r, g, b = p, value, t
        case 3: r, g, b = p, q, value
        case 4: r, g, b = t, p, value
        case 5: r, g, b = value, p, q
    }

    var red, green, blue uint8 = uint8(255 * r), uint8(255 * g), uint8(255 * b)
    return color.NRGBA{red, green, blue, 255}
}


func generatePalette(count int) (palette []color.Color) {
    palette = append(palette, color.Black)

    if count < 1 {
        return palette
    }

    const NUM_HUES = 360
    const MAX float64 = 1.0
    const MIN float64 = 0.5
    const SPREAD float64 = MAX - MIN

    var totalRounds int = count / NUM_HUES + 1

    var colorsPerRound int = (count + 1) / totalRounds
    var dH float64 = MAX / float64(colorsPerRound)

    var numValues int = squarestFactor(totalRounds)
    var dV float64 = SPREAD / float64(numValues)

    var numSaturations int = totalRounds / numValues
    var dS float64 = SPREAD / float64(numSaturations)

    var h, s, v float64 = 0, MIN, MIN
    for si := 0; si < numSaturations; si++ {
        for vi := 0; vi < numValues; vi++ {
            for h = 0; h < MAX; h += dH {
                var color = convertToRGB(h, s, v)
                palette = append(palette, color)
            }
            v += dV
        }
        s += dS
    }
    return palette
}


func squarestFactor(value int) int {
    var guess = int(math.Sqrt(float64(value)))
    for guess > 1 {
        if value % guess == 0 {
            return guess
        }
    }
    return value
}


func outOfBoundsChar(coord Coord) string {
    var x, y = coord[0], coord[1]
    if y < 0 {
        if x < 0 {
            return TOP_LEFT_CORNER
        } else if x > 127 {
            return TOP_RIGHT_CORNER
        } else {
            return HORIZONTAL
        }
    } else if y > 127 {
        if x < 0 {
            return BOTTOM_LEFT_CORNER
        } else if x > 127 {
            return BOTTOM_RIGHT_CORNER
        } else {
            return HORIZONTAL
        }
    } else if x < 0 {
        return LEFT_VERTICAL
    } else if x > 127 {
        return RIGHT_VERTICAL
    }
    panic(fmt.Errorf("wat"))
}


func printable(index int) string {
    const LOWER, UPPER = '\u4E00', '\u9FFF'
    var value = index % (UPPER - LOWER + 1) + LOWER
    return string(rune(value))
}


func getConnectedNeighbors(coord Coord) (neighbors []Coord) {
    for _, offset := range NEIGHBORS {
        var neighbor = move(coord, offset)
        if isInbounds(neighbor) {
            neighbors = append(neighbors, neighbor)
        }
    }
    return
}


func move(coord Coord, offset Coord) Coord {
    return Coord{coord[0] + offset[0], coord[1] + offset[1]}
}


func isInbounds(coord Coord) bool {
    return 0 <= coord[0] && coord[0] < 128 &&
           0 <= coord[1] && coord[1] < 128
}


func saveImage(image image.Image, filename string) {
    var fp, err = os.Create(filename)
    if err != nil {
        panic(err)
    }
    defer fp.Close()
    png.Encode(fp, image)
    fmt.Printf("Image written to %s\n", filename)
}


func main() {
    var keyString = os.Args[1]
    var grid = getDiskState(keyString)
    printGrid(grid, Coord{-1, -1}, Coord{128, 128})
    var numIslands, islands = countIslands(grid)
    printIslands(islands, Coord{-1, -1}, Coord{128, 128})
    fmt.Println(numIslands)
    var palette = generatePalette(numIslands)
    var image = drawIslands(islands, palette)
    saveImage(image, fmt.Sprintf("%s.png", keyString))
}
