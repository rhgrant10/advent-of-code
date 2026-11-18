//go:build ignore

package main

import "fmt"
import "bufio"
import "io"
import "os"
import "strings"
import "strconv"


func calculateChecksum(rows [][]int) (checksum int) {
    for _, row := range rows {
        min := row[0]
        max := row[0]
        for _, value := range row {
            if value < min {
                min = value
            } else if value > max {
                max = value
            }
        }
        checksum += max - min
    }
    return
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
