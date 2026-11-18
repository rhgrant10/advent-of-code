package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func part1(input []string) error {
	zero_count := 0
	position := 50
	for _, instr := range input {
		amount, err := strconv.Atoi(instr[1:])
		if err != nil {
			return err
		}
		amount %= 100
		if instr[0] == 'L' {
			amount = -amount
		}
		position += amount
		if position < 0 {
			position = 100 + position
		} else {
			position %= 100
		}
		if position == 0 {
			zero_count += 1
		}
	}
	fmt.Println(zero_count)
	return nil
}

func part2(input []string) error {
	zero_count := 0
	position := 50
	for _, instr := range input {
		amount, err := strconv.Atoi(instr[1:])
		if err != nil {
			return err
		}
		if amount == 0 {
			continue
		}
		extra_zeros := amount / 100
		zero_count += extra_zeros
		amount %= 100
		if instr[0] == 'L' {
			amount = -amount
		}
		position += amount
		if position <= 0 {
			if position != amount {
				zero_count += 1
			}
			position += 100
			position %= 100
		} else if position >= 100 {
			zero_count += 1
			position -= 100
		}
	}
	fmt.Println(zero_count)
	return nil
}

func main() {
	filename := os.Args[1]
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	input := strings.Split(strings.Trim(string(data), "\n "), "\n")
	part1(input)
	part2(input)
}
