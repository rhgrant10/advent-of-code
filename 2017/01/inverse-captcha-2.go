// inverse-captcha
package main

import "fmt"
import "io/ioutil"
import "os"
import "strconv"
import "strings"


func perform(captcha []int) (sum int) {
    var size = len(captcha)
    var j = size / 2
    for i := 0; i < size; i++ {
        if captcha[i] == captcha[j % size] {
            sum += captcha[i]
        }
        j++
    }
    return
}


func parseCaptcha(filename string) (captcha []int) {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }
    var sequence = strings.TrimSpace(string(data))
    for _, char := range sequence {
        var digit, err = strconv.Atoi(string(char))
        if err != nil {
            panic(err)
        }
        captcha = append(captcha, digit)
    }
    return
}


func main() {
    var filename = os.Args[1]
    var captcha = parseCaptcha(filename)
    fmt.Println(perform(captcha))
}
