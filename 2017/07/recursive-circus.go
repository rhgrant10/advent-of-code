package main

import "bufio"
import "fmt"
import "io"
import "os"
import "strconv"
import "strings"


func parseTree(filename string) (map[string]string, map[string]int) {
    fp, err := os.Open(filename)
    if err != nil {
        panic(err)
    }
    defer fp.Close()

    parents := make(map[string]string)
    weights := make(map[string]int)

    reader := bufio.NewReader(fp)
    for {
        line, err := reader.ReadString('\n')
        if err != nil {
            if err == io.EOF {
                break
            }
            panic(err)
        }

        fields := strings.Fields(line)
        node := fields[0]
        weightField := fields[1]
        weight, err := strconv.Atoi(weightField[1:len(weightField) - 1])
        if err != nil {
            panic(err)
        }
        weights[node] = weight

        if strings.Contains(line, "->") {
            for _, childField := range fields[3:] {
                child := strings.Trim(childField, ",")
                parents[child] = node
            }
        }
    }

    return parents, weights
}


func findRoot(parents map[string]string, weights map[string]int) (string, error) {
    for node, _ := range weights {
        _, present := parents[node]
        if !present {
            return node, nil
        }
    }
    var noRoot string
    return noRoot, fmt.Errorf("No root found! You sure this is a tree?")
}


func main() {
    filename := os.Args[1]
    parents, nodes := parseTree(filename)
    root, err := findRoot(parents, nodes)
    if err != nil {
        panic(err)
    }
    fmt.Println(root)
}
