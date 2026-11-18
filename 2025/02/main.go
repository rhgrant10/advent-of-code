package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	low  int
	high int
}

func getDigitCount(n int) int {
	return int(math.Log10(float64(n)) + 1)
}

func repeat(s string, n int) string {
	sb := strings.Builder{}
	for range n {
		sb.WriteString(s)
	}
	return sb.String()
}

func isInvalidID(n int, maxPieces int) bool {
	digitCount := getDigitCount(n)
	s := strconv.Itoa(n)
	for pieces := 2; pieces <= maxPieces; pieces++ {
		if digitCount%pieces == 0 {
			part := s[:digitCount/pieces]
			whole := repeat(part, pieces)
			if whole == s {
				return true
			}
		}
	}
	return false
}

func part1(ranges []Range) {
	var total int

	for _, r := range ranges {
		for n := r.low; n <= r.high; n++ {
			if isInvalidID(n, 2) {
				total += n
			}
		}
	}

	fmt.Println(total)
}

func part2(ranges []Range) {
	var total int

	for _, r := range ranges {
		for n := r.low; n <= r.high; n++ {
			if isInvalidID(n, getDigitCount(n)) {
				total += n
			}
		}
	}

	fmt.Println(total)
}

func parse(filename string) []Range {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	var ranges []Range
	for rstr := range strings.SplitSeq(strings.Trim(string(data), "\n "), ",") {
		parts := strings.Split(rstr, "-")
		low, err := strconv.Atoi(parts[0])
		if err != nil {
			panic(err)
		}
		high, err := strconv.Atoi(parts[1])
		if err != nil {
			panic(err)
		}
		ranges = append(ranges, Range{low, high})
	}
	return ranges
}

func main() {
	filename := os.Args[1]
	ranges := parse(filename)
	part1(ranges)
	part2(ranges)
}
