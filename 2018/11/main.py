

def calculate_fuel_grid(serial_no, size):
    grid = []
    for y in range(size):
        row = []
        for x in range(size):
            power = get_power_level(x, y, serial_no)
            row.append(power)
        grid.append(row)
    return grid


def get_power_level(x, y, serial_no):
    rack_id = (x + 1) + 10
    power = rack_id * (y + 1) + serial_no
    power *= rack_id
    hundreds = power // 100 % 10
    power = hundreds - 5
    return power


def find_max_location(grid, window):
    greatest = None
    top_left = None
    for y in range(len(grid) - window):
        for x in range(len(grid[y]) - window):
            power = 0
            for dy in range(window):
                for dx in range(window):
                    power += grid[y + dy][x + dx]

            if greatest is None or greatest < power:
                greatest = power
                top_left = x, y
    return top_left


def find_max_window(grid):
    max_sum = top_left = size = None

    length = len(grid)
    for left in range(length):
        dp = [0] * length
        for right in range(left, length):
            width = right - left + 1
            for i in range(length):
                dp[i] += grid[i][right]
            sum_, start = find_max_sum(dp, width)
            if max_sum is None or sum_ >= max_sum:
                max_sum = sum_
                top_left = left, start
                size = width

    return top_left, size


def find_max_sum(arr, size):
    max_sum = sum_ = sum(arr[:size])
    start = 0
    i = 0
    while i < len(arr) - size:
        sum_ += arr[size + i] - arr[i]
        if sum_ > max_sum:
            max_sum = sum_
            start = i + 1
        i += 1
    return max_sum, start


def part_1(input_):
    serial_number = int(input_.strip())
    grid = calculate_fuel_grid(serial_number, size=300)
    x, y = find_max_location(grid, window=3)
    return f'{x + 1},{y + 1}'


def part_2(input_):
    serial_number = int(input_.strip())
    grid = calculate_fuel_grid(serial_number, size=300)
    (x, y), w = find_max_window(grid)
    return f'{x + 1},{y + 1},{w}'
