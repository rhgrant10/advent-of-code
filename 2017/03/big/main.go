// big-spiral-memory
package main

import "fmt"
import "io/ioutil"
import "os"
import "math/big"


// see spiral-memory.go for an explanation of the algorithm
func calculateSpiralManhattan(square *big.Int) *big.Int {
    zero := big.NewInt(0)
    one := big.NewInt(1)
    two := big.NewInt(2)

    if square.Cmp(one) == 0 {
        return zero
    }

    // Make serious use of a temp variable
    t := new(big.Int)

    // squareFloor := int(math.Sqrt(float64(square - 1)))
    t.Sub(square, one)
    squareFloor := new(big.Int).Sqrt(t)

    // ringMaxRoot := squareFloor + (squareFloor % 2) + 1
    t.Mod(squareFloor, two)
    t.Add(t, one)
    ringMaxRoot := new(big.Int).Add(t, squareFloor)

    // ringMax := int(math.Pow(float64(ringMaxRoot), 2))
    ringMax := new(big.Int).Exp(ringMaxRoot, two, nil)

    // ringId := (ringMaxRoot + 1) / 2 - 1
    t.Add(ringMaxRoot, one)
    t.Div(t, two)
    ringId := new(big.Int).Sub(t, one)

    // ringSize := ringMax - int(math.Pow(math.Sqrt(float64(ringMax)) - 2, 2))
    t.Sqrt(ringMax)
    t.Sub(t, two)
    t.Exp(t, two, nil)
    ringSize := new(big.Int).Sub(ringMax, t)

    // edgeIndex := ringSize - (ringMax - square)
    t.Sub(ringMax, square)
    edgeIndex := new(big.Int).Sub(ringSize, t)

    // perpendicular := int(math.Abs(float64(edgeIndex % (ringId * 2) - ringId)))
    t.Mul(ringId, two)
    t.Mod(edgeIndex, t)
    t.Sub(t, ringId)
    perpendicular := new(big.Int).Abs(t)

    // distance := ringId + perpendicular
    distance := t.Add(ringId, perpendicular)
    return distance
}


func readSquare(filename string) *big.Int {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    var square = new(big.Int)
    _, ok := square.SetString(string(data), 10)
    if !ok {
        panic(fmt.Errorf("could not parse integer"))
    }
    return square
}


func main() {
    var square = readSquare(os.Args[1])
    var distance = calculateSpiralManhattan(square)
    fmt.Println(distance)
}
