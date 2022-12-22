import itertools
import re

lines = open("../inputs/day_22.txt", "r").read().splitlines()

field = []
for y, line in enumerate(lines[:-2]):
    field.append([])
    for x, c in enumerate(line):
        if c != ' ':
            field[-1].append((x, y, c))

max_x = max(point[0] for point in itertools.chain(*field))
max_y = max(point[1] for point in itertools.chain(*field))

rotation = {
    ("L", "R"): "U", ("L", "U"): "L", ("L", "L"): "D", ("L", "D"): "R",
    ("R", "R"): "D", ("R", "U"): "R", ("R", "L"): "U", ("R", "D"): "L"
}

# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
facing_cost = {"R": 0, "D": 1, "L": 2, "U": 3}
def move(direction, x, y, field):
    if direction == "D":
        next_y = y + 1
        if next_y > max_y or not any(point[0] == x for point in field[next_y]):
            for y in range(0, max_y):
                if any(point[0] == x for point in field[y]):
                    return x, y
        else:
            return x, next_y
    if direction == "U":
        next_y = y - 1
        if next_y < 0 or not any(point[0] == x for point in field[next_y]):
            for y in range(max_y, 0, -1):
                if any(point[0] == x for point in field[y]):
                    return x, y
        else:
            return x, next_y
    if direction == "R":
        next_x = x + 1
        if not any(point[0] == next_x for point in field[y]):
            return field[y][0][0], y
        else:
            return next_x, y
    if direction == "L":
        next_x = x - 1
        if not any(point[0] == next_x for point in field[y]):
            return field[y][-1][0], y
        else:
            return next_x, y

def check_point(x, y):
    checking_point = [point for point in field[y] if point[0] == x][0]
    return checking_point[2] != '#'

y = 0
x = field[y][0][0]
direction = 'R'

directions = [c for c in lines[-1] if c in ('R', 'L')]
steps = [int(steps) for steps in re.split('L|R', lines[-1])]

directions_idx = 0
for steps_count in steps:
    current_steps = 0
    while(current_steps < steps_count):
        next_x, next_y = move(direction=direction, x=x, y=y, field=field)
        if check_point(next_x, next_y):
            x, y = next_x, next_y
            current_steps = current_steps + 1
        else:
            break
    if (directions_idx < len(directions)):
        direction = rotation[directions[directions_idx], direction]
        directions_idx = directions_idx + 1
    print(x + 1, y + 1, direction)
    print((x + 1) * 4 + (y + 1) * 1000 + facing_cost[direction])

# The final password is the sum of 1000 times the row, 4 times the column, and the facing.