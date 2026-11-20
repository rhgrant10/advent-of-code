package main

import (
	"fmt"
	"os"
)

type Point struct {
	r, c int
}

func (p Point) Add(q Point) Point {
	return Point{p.r + q.r, p.c + q.c}
}

func (p Point) IsBetween(min, max Point) bool {
	return min.r <= p.r && p.r < max.r && min.c <= p.c && p.c < max.c
}

func (p Point) On(grid [][]byte) byte {
	return grid[p.r][p.c]
}

func (p Point) MakeGrid() [][]byte {
	grid := make([][]byte, p.r)
	for i := range p.r {
		grid[i] = make([]byte, p.c)
	}
	return grid
}

var dirs = []Point{
	{-1, -1},
	{0, -1},
	{1, -1},
	{1, 0},
	{1, 1},
	{0, 1},
	{-1, 1},
	{-1, 0},
}

func part1(grid [][]byte) {
	count := 0
	min := Point{}
	max := Point{len(grid), len(grid[0])}
	for r := range max.r {
		for c := range max.c {
			if grid[r][c] != '@' {
				continue
			}
			n := 0
			for _, d := range dirs {
				p := Point{r, c}.Add(d)
				if p.IsBetween(min, max) && p.On(grid) == '@' {
					n += 1
				}
			}
			if n < 4 {
				count += 1
			}
		}
	}

	fmt.Println(count)
}

func part2(grid [][]byte) {
	min := Point{}
	max := Point{len(grid), len(grid[0])}
	count := 0

	var newGrid [][]byte
	for {
		removed := 0
		newGrid = max.MakeGrid()
		for r := range max.r {
			for c := range max.c {
				if grid[r][c] != '@' {
					newGrid[r][c] = grid[r][c]
					continue
				}
				n := 0
				for _, d := range dirs {
					p := Point{r, c}.Add(d)
					if p.IsBetween(min, max) && p.On(grid) == '@' {
						n += 1
					}
				}
				if n < 4 {
					removed += 1
					newGrid[r][c] = '.'
				} else {
					newGrid[r][c] = '@'
				}
			}
		}
		if removed == 0 {
			break
		}
		count += removed
		grid = newGrid
	}

	fmt.Println(count)
}

func parse(filename string) [][]byte {
	var grid [][]byte
	body, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	var row []byte
	for _, c := range body {
		if c == '\n' {
			grid = append(grid, row)
			row = make([]byte, 0)
		} else {
			row = append(row, c)
		}
	}
	if len(row) > 0 {
		grid = append(grid, row)
	}
	return grid
}

func main() {
	filename := os.Args[1]
	input := parse(filename)
	part1(input)
	part2(input)
}
