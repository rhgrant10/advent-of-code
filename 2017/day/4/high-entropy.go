package main

import "fmt"
import "os"
import "io/ioutil"
import "strings"


func isValid(passphrase string) bool {
    words := strings.Split(passphrase, " ")
    seen := make(map[string]bool)
    for _, word := range words {
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
