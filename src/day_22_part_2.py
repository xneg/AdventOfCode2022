import re

from src.utils import chunker


class CubeSurface:
    def __init__(self, points):
        self.surface_up = []
        for y, line in enumerate(points):
            self.surface_up.append([])
            for x, point in enumerate(line):
                self.surface_up[-1].append(point)
        self.surface_left = list(map(list, zip(*reversed(self.surface_up))))
        self.surface_down = list(map(list, zip(*reversed(self.surface_left))))
        self.surface_right = list(map(list, zip(*reversed(self.surface_down))))
        self.direct_surfaces = {
            "U": self.surface_up,
            "L": self.surface_left,
            "D": self.surface_down,
            "R": self.surface_right
        }
        self.number = None


lines = open("../inputs/day_22.txt", "r").read().splitlines()

size = 50
surfaces = []
for block in chunker(lines[:-2], size):
    aux = [list(chunker(line, size)) for line in block]
    surfaces_list = list(map(list, zip(*reversed(aux))))
    surfaces.extend([CubeSurface(list(reversed(s))) for s in surfaces_list if s[0] != ' ' * size])

for idx, surface in enumerate(surfaces):
    surface.number = idx

neighbors = {
    (0, 'U'): (2, 'U'),
    (0, 'D'): (5, 'L'),
    (0, 'L'): (1, 'L'),
    (0, 'R'): (3, 'L'),

    (1, 'U'): (2, 'R'),
    (1, 'D'): (5, 'D'),
    (1, 'L'): (4, 'R'),
    (1, 'R'): (0, 'R'),

    (2, 'U'): (4, 'U'),
    (2, 'D'): (0, 'D'),
    (2, 'L'): (1, 'D'),
    (2, 'R'): (3, 'U'),

    (3, 'U'): (5, 'U'),
    (3, 'D'): (2, 'L'),
    (3, 'L'): (4, 'L'),
    (3, 'R'): (0, 'L'),

    (4, 'U'): (5, 'R'),
    (4, 'D'): (2, 'D'),
    (4, 'L'): (1, 'R'),
    (4, 'R'): (3, 'R'),

    (5, 'U'): (1, 'U'),
    (5, 'D'): (3, 'D'),
    (5, 'L'): (4, 'D'),
    (5, 'R'): (0, 'U'),
}


rotation = {"L": lambda x, y: (size - y - 1, x), "R": lambda x, y: (y, size - x - 1)}
def move(x, y, current_surface, surface_direction):
    next_y = y + 1
    if next_y > size - 1:
        surface_idx, new_direction = neighbors[(current_surface.number, surface_direction)]
        return x, 0, surfaces[surface_idx], new_direction
    else:
        return x, next_y, current_surface, surface_direction

def check_point(x, y, surface, direction):
    checking_point = surface.direct_surfaces[direction][y][x]
    return checking_point != '#'

def get_next_direction(current_direction, rotation):
    directions_enum = ["U", "L", "D", "R"]
    idx = directions_enum.index(current_direction)
    idx = idx + 1 if rotation == 'L' else idx - 1
    if idx == len(directions_enum): return directions_enum[0]
    if idx < 0: return directions_enum[-1]
    return directions_enum[idx]

y = 0
x = 0
current_surface = surfaces[0]
direction = 'L'
x, y = rotation[direction](x, y)

rotations = [c for c in lines[-1] if c in ('R', 'L')]
steps = [int(steps) for steps in re.split('L|R', lines[-1])]

rotations_idx = 0
for steps_count in steps:
    current_steps = 0
    while current_steps < steps_count:
        next_x, next_y, next_surface, next_direction = \
            move(x=x, y=y, current_surface=current_surface, surface_direction=direction)
        if check_point(next_x, next_y, next_surface, next_direction):
            x, y = next_x, next_y
            current_surface = next_surface
            direction = next_direction
            current_steps = current_steps + 1
        else:
            break
    if rotations_idx < len(rotations):
        current_rotation = rotations[rotations_idx]
        x, y = rotation[current_rotation](x, y)
        direction = get_next_direction(direction, current_rotation)
        rotations_idx = rotations_idx + 1
    print(x, y, direction, current_surface.number)

x, y = rotation["R"](x, y)
direction =  get_next_direction(direction, "R")

facing_cost = {"R": 0, "D": 1, "L": 2, "U": 3}
print(x, y, direction, current_surface.number)
print((x + 1) * 4 + (y + 1 + size * 2) * 1000 + facing_cost["R"])