package main

import (
	"bytes"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type MathOp func(a, b int) int

func add(a, b int) int { return a + b }
func mul(a, b int) int { return a * b }

type Problem struct {
	values []int
	opcode byte
}

func (p Problem) opFunc() MathOp {
	switch p.opcode {
	case '*':
		return mul
	case '+':
		return add
	default:
		panic(fmt.Sprintf("unknown opcode %v", p.opcode))
	}
}

func (p Problem) intialValue() int {
	switch p.opcode {
	case '*':
		return 1
	case '+':
		return 0
	default:
		panic(fmt.Sprintf("unknown opcode %v", p.opcode))
	}
}

func (p Problem) Answer() int {
	f := p.opFunc()
	a := p.intialValue()
	for _, v := range p.values {
		a = f(a, v)
	}
	return a
}

func part1(problems []Problem) {
	total := 0
	for _, p := range problems {
		total += p.Answer()
	}
	fmt.Println(total)
}

func part2(problems []Problem) {
	total := 0
	for _, p := range problems {
		total += p.Answer()
	}
	fmt.Println(total)
}

func parse1(filename string) []Problem {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	text := strings.Trim(string(bytes), "\n ")
	lines := strings.Split(text, "\n")

	var operandRows [][]int
	for _, line := range lines[0 : len(lines)-1] {
		var operandRow []int
		for field := range strings.FieldsSeq(line) {
			operand, err := strconv.Atoi(field)
			if err != nil {
				panic(err)
			}
			operandRow = append(operandRow, operand)
		}
		operandRows = append(operandRows, operandRow)
	}

	opLine := lines[len(lines)-1]
	var opRow []byte
	for field := range strings.FieldsSeq(opLine) {
		opRow = append(opRow, field[0])
	}

	var problems []Problem
	for c := 0; c < len(opRow); c++ {
		var values []int
		for r := range len(operandRows) {
			values = append(values, operandRows[r][c])
		}
		problems = append(problems, Problem{values, opRow[c]})
	}

	return problems
}

func parse2(filename string) (problems []Problem) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	var byteGrid [][]byte
	for byteRow := range bytes.SplitSeq(data, []byte("\n")) {
		if len(byteRow) > 0 {
			byteGrid = append(byteGrid, byteRow)
		}
	}

	length := 0
	for _, row := range byteGrid {
		if length < len(row) {
			length = len(row)
		}
	}
	for r := range byteGrid {
		for length > len(byteGrid[r]) {
			byteGrid[r] = append(byteGrid[r], ' ')
		}
	}

	var value int
	var values []int
	var opcode byte
	for c := len(byteGrid[0]); c > 0; c-- {
		for r := 0; r < len(byteGrid); r++ {
			switch char := byteGrid[r][c-1]; char {
			case '*', '+':
				opcode = char
			case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
				value *= 10
				value += int(char - '0')
			}
		}
		if value > 0 {
			values = append(values, value)
			value = 0
		}
		if opcode > 0 {
			problems = append(problems, Problem{values, opcode})
			values = make([]int, 0)
			opcode = 0
		}
	}
	return
}

func main() {
	filename := os.Args[1]
	problems1 := parse1(filename)
	problems2 := parse2(filename)
	// fmt.Printf("%v\n\n%v\n", problems)
	part1(problems1)
	part2(problems2)
}
