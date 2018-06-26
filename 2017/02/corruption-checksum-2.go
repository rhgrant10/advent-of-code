package main

import "fmt"
import "bufio"
import "io"
import "os"
import "strings"
import "strconv"


func calculateChecksum(rows [][]int) (checksum int) {
    for _, row := range rows {
        checksum += calculateRowValue(row)
    }
    return
}


func calculateRowValue(row []int) int {
    for i := 0; i < len(row); i++ {
        for j := i + 1; j < len(row); j++ {
            small, large := row[i], row[j]
            if small > large {
                small, large = large, small
            }
            if large % small == 0 {
                return large / small
            }
        }
    }
    return 0
}


func readSpreadsheet(filename string) (spreadsheet [][]int) {
    fp, err := os.Open(filename)
    if err != nil {
        panic(err)
    }
    defer fp.Close()

    var reader = bufio.NewReader(fp)
    for {
        line, err := reader.ReadString('\n')
        if err != nil {
            if err == io.EOF {
                break
            }
            panic(err)
        }

        var row []int
        for _, field := range strings.Fields(line) {
            n, err := strconv.Atoi(field)
            if err != nil {
                panic(err)
            }
            row = append(row, n)
        }
        spreadsheet = append(spreadsheet, row)
    }
    return
}


func main() {
    var filename = os.Args[1]
    var spreadsheet = readSpreadsheet(filename)
    var checksum = calculateChecksum(spreadsheet)
    fmt.Println(checksum)
}