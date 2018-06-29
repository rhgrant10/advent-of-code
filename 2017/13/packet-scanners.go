package main

import "fmt"
import "io/ioutil"
import "os"
import "strings"
import "strconv"


func toInt(s string) int {
    i, err := strconv.Atoi(strings.TrimSpace(s))
    if err != nil {
        panic(err)
    }
    return i
}


func readFirewall(filename string) map[int]int {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    var content = strings.TrimSpace(string(data))
    var lines = strings.Split(content, "\n")

    var firewall = make(map[int]int, 0)
    for _, line := range lines {
        var keypair = strings.Split(line, ":")
        var depth = toInt(keypair[0])
        var range_ = toInt(keypair[1])
        firewall[depth] = range_
    }

    return firewall
}


func cross(firewall map[int]int) int {
    var cost = 0
    for depth, range_ := range firewall {
        var period = 2 * (range_ - 1)
        if depth % period == 0 {
            cost += depth * range_
        }
    }
    return cost
}


func main() {
    var filename = os.Args[1]
    var firewall = readFirewall(filename)
    var cost = cross(firewall)
    fmt.Println(cost)
}