package main

import (
	"fmt"
	"os"
	"strings"
)

type Bank []int

func getVoltageSum(banks []Bank, batteryCount int) int64 {
	var voltageSum int64
	for _, bank := range banks {
		var voltage int64
		right := len(bank) - batteryCount + 1
		left := 0
		for range batteryCount {
			digit := 0
			for i := left; i < right; i++ {
				if bank[i] > digit {
					digit = bank[i]
					left = i + 1
				}
			}
			right += 1
			voltage *= 10
			voltage += int64(digit)
		}
		voltageSum += voltage
	}
	return voltageSum
}

func part1(banks []Bank) {
	voltageSum := getVoltageSum(banks, 2)
	fmt.Println(voltageSum)
}

func part2(banks []Bank) {
	voltageSum := getVoltageSum(banks, 12)
	fmt.Println(voltageSum)
}

func parse(filename string) []Bank {
	var banks []Bank
	body, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	text := strings.Trim(string(body), "\n ")
	for line := range strings.SplitSeq(text, "\n") {
		var bank Bank
		for _, c := range line {
			bank = append(bank, int(c-'0'))
		}
		banks = append(banks, bank)
	}
	return banks
}

func main() {
	filename := os.Args[1]
	input := parse(filename)
	part1(input)
	part2(input)
}
