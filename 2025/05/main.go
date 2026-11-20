package main

import (
	"cmp"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Range struct {
	min, max int
}

func part1(fresh []Range, available []int) {
	count := 0
	for _, ingredient := range available {
		for _, r := range fresh {
			if r.min <= ingredient && ingredient <= r.max {
				count += 1
				break
			}
		}
	}
	fmt.Println(count)
}

func part2(fresh []Range, _ []int) {
	slices.SortFunc(fresh, func(a, b Range) int {
		return cmp.Compare(a.min, b.min)
	})
	combined := []Range{fresh[0]}
	for _, r := range fresh[1:] {
		end := &combined[len(combined)-1]
		if r.min <= end.max {
			if end.max < r.max {
				end.max = r.max
			}
		} else {
			combined = append(combined, r)
		}
	}

	count := 0
	for _, r := range combined {
		size := r.max + 1 - r.min
		count += size
	}
	fmt.Println(count)
}

func parse(filename string) ([]Range, []int) {
	var fresh []Range
	var available []int

	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	parsingFresh := true
	for line := range strings.SplitSeq(strings.Trim(string(bytes), " \n"), "\n") {
		if len(line) == 0 {
			parsingFresh = false
			continue
		}
		if parsingFresh {
			parts := strings.Split(line, "-")
			min, err := strconv.Atoi(parts[0])
			if err != nil {
				panic(err)
			}
			max, err := strconv.Atoi(parts[1])
			if err != nil {
				panic(err)
			}
			fresh = append(fresh, Range{min, max})
		} else {
			ingredient, err := strconv.Atoi(line)
			if err != nil {
				panic(err)
			}
			available = append(available, ingredient)
		}
	}

	return fresh, available
}

func main() {
	filename := os.Args[1]
	fresh, available := parse(filename)
	// fmt.Printf("%v\n\n%v\n", fresh, available)
	part1(fresh, available)
	part2(fresh, available)
}
