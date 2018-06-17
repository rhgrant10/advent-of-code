package main

import "fmt"
import "os"
import "io/ioutil"
import "strings"
import "sort"

type Runes []rune

func (r Runes) Len() int { return len(r) }
func (r Runes) Swap(i, j int) { r[j], r[i] = r[i], r[j] }
func (r Runes) Less(i, j int) bool { return r[i] < r[j] }


func sortedString(s string) string {
    var runes Runes
    for _, r := range s {
        runes = append(runes, r)
    }
    sort.Sort(runes)
    return string(runes)
}


func isValid(passphrase string) bool {
    words := strings.Split(passphrase, " ")
    seen := make(map[string]bool)
    for _, word := range words {
        word = sortedString(word)
        if seen[word] == true {
            return false
        }
        seen[word] = true
    }
    return true
}


func main() {
    data, err := ioutil.ReadFile(os.Args[1])
    if err != nil {
        panic(err)
    }
    contents := strings.Trim(string(data), "\n")
    passphrases := strings.Split(contents, "\n")
    numValid := 0
    for _, passphrase := range passphrases {
        if isValid(passphrase) {
            numValid += 1
        }
    }

    fmt.Println(numValid)
}
