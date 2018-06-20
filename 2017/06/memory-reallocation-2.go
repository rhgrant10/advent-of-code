package main

import "fmt"
import "os"
import "io/ioutil"
import "strings"
import "strconv"


func readBanks(data string) (banks []int) {
    fields := strings.Fields(string(data))
    for _, field := range fields {
        bank, err := strconv.Atoi(field)
        if err != nil {
            panic(err)
        }
        banks = append(banks, bank)
    }
    return
}


func writeData(banks []int) string {
    var elements []string
    for _, bank := range banks {
        elements = append(elements, strconv.Itoa(bank))
    }
    return strings.Join(elements, "\t")
}


func redistribute(data string) string {
    banks := readBanks(data)

    // find the largest bank and it's index
    var index, maxBlocks int
    for i, blocks := range banks {
        if blocks > maxBlocks {
            index = i
            maxBlocks = blocks
        }
    }

    // redistrubte the largest bank
    banks[index] = 0
    for maxBlocks > 0 {
        index = (index + 1) % len(banks)
        banks[index] += 1
        maxBlocks -= 1
    }

    return writeData(banks)
}


func countReallocationCycles(banks string) (count int) {
    seen := make(map[string]bool)

    hasKey := false
    for !hasKey {
        seen[banks] = true
        banks = redistribute(banks)
        _, hasKey = seen[banks];
    }

    count = 1
    target := banks
    banks = redistribute(banks)
    for banks != target {
        banks = redistribute(banks)
        count += 1
    }

    return
}


func parseInputFile(filename string) string {
    data, err := ioutil.ReadFile(os.Args[1])
    if err != nil {
        panic(err)
    }
    return writeData(readBanks(string(data)))
}


func main() {
    banks := parseInputFile(os.Args[1])
    count := countReallocationCycles(banks)
    fmt.Println(count)
}
