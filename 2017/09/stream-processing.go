package main

import "fmt"
import "os"
import "io/ioutil"
import "strings"


type StateError struct {
    char rune
    transition string
}

func (e *StateError) Error() string {
    return fmt.Sprintf("bad char '%v' for transition %s", e.char, e.transition)
}


type Transition func(state *state) (Transition, error)


type state struct {
    Scores []int
    Level int
    Stream chan rune
}


func NewState(data string) *state {
    var stream = make(chan rune)
    go func() {
        defer close(stream)
        for _, char := range data {
            stream <- char
        }
        stream <- 0
    }()
    return &state{Stream: stream}
}


func readInputFile(filename string) string {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        panic(err)
    }

    return strings.Trim(string(data), "\n")
}


func start(state *state) (Transition, error) {
    char := <-state.Stream
    switch {
    case char == '{':
        return newGroup, nil
    default:
    }
    return nil, &StateError{char, "start"}
}


func newGroup(state *state) (Transition, error) {
    state.Level += 1
    state.Scores = append(state.Scores, state.Level)
    char := <-state.Stream
    switch {
    case char == '{':
        return newGroup, nil
    case char == '<':
        return garbage, nil
    case char == '}':
        return endGroup, nil
    default:
    }
    return nil, &StateError{char, "newGroup"}
}


func garbage(state *state) (Transition, error) {
    char := <- state.Stream
    switch {
    case char == '!':
        return ignore, nil
    case char == '>':
        return endGarbage, nil
    case char == 0:
        return nil, &StateError{char, "garbage"}
    default:
        return garbage, nil
    }
}


func ignore(state *state) (Transition, error) {
    _ = <- state.Stream
    return garbage, nil
}


func endGarbage(state *state) (Transition, error) {
    char := <- state.Stream
    switch {
    case char == ',':
        return nextThing, nil
    case char == '}':
        return endGroup, nil
    default:
        return nil, &StateError{char, "endGarbage"}
    }
}


func nextThing(state *state) (Transition, error) {
    char := <- state.Stream
    switch {
    case char == '{':
        return newGroup, nil
    case char == '<':
        return garbage, nil
    default:
        return nil, &StateError{char, "nextThing"}
    }
}


func endGroup(state *state) (Transition, error) {
    state.Level -= 1
    char := <-state.Stream
    switch {
    case char == 0:
        return nil, nil  // we're done
    case char == '{':
        return newGroup, nil
    case char == ',':
        return nextThing, nil
    case char == '}':
        return endGroup, nil
    default:
        return nil, &StateError{char, "endGroup"}
    }
}


func getScores(stream string) []int {
    var state = NewState(stream)

    transition, err := start(state)
    for transition != nil || err != nil {
        transition, err = transition(state)
    }
    if err != nil {
        panic(err)
    }
    return state.Scores
}


func sum(numbers []int) (total int) {
    for _, n := range numbers {
        total += n
    }
    return
}


func main() {
    var filename = os.Args[1]
    var stream = readInputFile(filename)
    var scores = getScores(stream)
    fmt.Println(sum(scores))
}
