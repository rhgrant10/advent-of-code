# GRID_SERIAL_NO = 3628
TOP = 1
LEFT = 1


def calculate_fuel_grid(serial_no, size):
    num_columns, num_rows = size
    grid = []
    for y in range(num_rows):
        row = []
        for x in range(num_columns):
            power = get_power_level(x, y, serial_no)
            row.append(power)
        grid.append(row)
    return grid


def get_power_level(x, y, serial_no):
    rack_id = (x + LEFT) + 10
    power = rack_id * (y + TOP) + serial_no
    power *= rack_id
    hundreds = power // 100 % 10
    power = hundreds - 5
    return power


def get_largest_total_power(grid, window):
    greatest = None
    top_left = None
    wx, wy = window
    for y in range(len(grid) - wy):
        for x in range(len(grid[y]) - wx):
            power = 0
            for dy in range(wy):
                for dx in range(wx):
                    power += grid[y + dy][x + dx]

            if greatest is None or power > greatest:
                greatest = power
                top_left = x, y
    x, y = top_left
    return x + LEFT, y + TOP


def part_1(input_):
    serial_number = int(input_.strip())
    grid = calculate_fuel_grid(serial_number, size=(300, 300))
    x, y = get_largest_total_power(grid, window=(3, 3))
    return f'{x}, {y}'
