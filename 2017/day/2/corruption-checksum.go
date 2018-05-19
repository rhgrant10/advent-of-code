// corruption-checksum
package main

import "fmt"


func get_spreadsheet() [][]int {
    rows := make([][]int, 0)
    rows = append(rows, []int{5, 1, 9, 5})
    rows = append(rows, []int{7, 5, 3})
    rows = append(rows, []int{2, 4, 6, 8})
    return rows
}


func get_square_spreadsheet() [][]int {
    rows := make([][]int, 0)
    rows = append(rows, []int{5, 9, 2, 8})
    rows = append(rows, []int{9, 4, 7, 3})
    rows = append(rows, []int{3, 8, 6, 5})
    return rows
}


func get_big_spreadsheet() [][]int {
    rows := make([][]int, 0)
    rows = append(rows, []int{4168, 3925, 858, 2203, 440, 185, 2886, 160, 1811, 4272, 4333, 2180, 174, 157, 361, 1555})
    rows = append(rows, []int{150, 111, 188, 130, 98, 673, 408, 632, 771, 585, 191, 92, 622, 158, 537, 142})
    rows = append(rows, []int{5785, 5174, 1304, 3369, 3891, 131, 141, 5781, 5543, 4919, 478, 6585, 116, 520, 673, 112})
    rows = append(rows, []int{5900, 173, 5711, 236, 2920, 177, 3585, 4735, 2135, 2122, 5209, 265, 5889, 233, 4639, 5572})
    rows = append(rows, []int{861, 511, 907, 138, 981, 168, 889, 986, 980, 471, 107, 130, 596, 744, 251, 123})
    rows = append(rows, []int{2196, 188, 1245, 145, 1669, 2444, 656, 234, 1852, 610, 503, 2180, 551, 2241, 643, 175})
    rows = append(rows, []int{2051, 1518, 1744, 233, 2155, 139, 658, 159, 1178, 821, 167, 546, 126, 974, 136, 1946})
    rows = append(rows, []int{161, 1438, 3317, 4996, 4336, 2170, 130, 4987, 3323, 178, 174, 4830, 3737, 4611, 2655, 2743})
    rows = append(rows, []int{3990, 190, 192, 1630, 1623, 203, 1139, 2207, 3994, 1693, 1468, 1829, 164, 4391, 3867, 3036})
    rows = append(rows, []int{116, 1668, 1778, 69, 99, 761, 201, 2013, 837, 1225, 419, 120, 1920, 1950, 121, 1831})
    rows = append(rows, []int{107, 1006, 92, 807, 1880, 1420, 36, 1819, 1039, 1987, 114, 2028, 1771, 25, 85, 430})
    rows = append(rows, []int{5295, 1204, 242, 479, 273, 2868, 3453, 6095, 5324, 6047, 5143, 293, 3288, 3037, 184, 987})
    rows = append(rows, []int{295, 1988, 197, 2120, 199, 1856, 181, 232, 564, 1914, 1691, 210, 1527, 1731, 1575, 31})
    rows = append(rows, []int{191, 53, 714, 745, 89, 899, 854, 679, 45, 81, 726, 801, 72, 338, 95, 417})
    rows = append(rows, []int{219, 3933, 6626, 2137, 3222, 1637, 5312, 238, 5895, 222, 154, 6649, 169, 6438, 3435, 4183})
    rows = append(rows, []int{37, 1069, 166, 1037, 172, 258, 1071, 90, 497, 1219, 145, 1206, 143, 153, 1067, 510})
    return rows
}


func calculate_checksum(rows [][]int) int {
    checksum := 0
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
    return checksum
}


func calculate_divides_checksum(rows [][]int) int {
    checksum := 0
    for _, row := range rows {
        ThisRow:
        for i := 0; i < len(row); i++ {
            for j := i + 1; j < len(row); j++ {
                large := row[i]
                small := row[j]
                if small > large {
                    small = row[i]
                    large = row[j]
                }
                if large % small == 0 {
                    checksum += large / small
                    break ThisRow
                }
            }
        }
    }
    return checksum
}


func main() {
    spreadsheet := get_big_spreadsheet()
    checksum := calculate_divides_checksum(spreadsheet)
    fmt.Println("checksum is ", checksum)
}