from dataclasses import dataclass
from src.utils import sign

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class RockPath:
    def __init__(self, points):
        self.points = [Point(point[0], point[1]) for point in points]

    def max_x(self):
        return max([point.x for point in self.points])

    def min_x(self):
        return min([point.x for point in self.points])

    def max_y(self):
        return max([point.y for point in self.points])

    def min_y(self):
        return min([point.y for point in self.points])

    def path(self):
        result = set()
        for idx, point in enumerate(self.points[:-1]):
            aux = Point(point.x, point.y)
            next = self.points[idx + 1]
            while aux != next:
                result.add(Point(aux.x, aux.y))
                aux = Point(aux.x + sign(next.x - aux.x), aux.y + sign(next.y - aux.y))
        result.add(Point(self.points[-1].x, self.points[-1].y))
        return result


def sand_move(field):
    sand_position = Point(sand_source.x, sand_source.y)
    if field[sand_position.y][sand_position.x] == 'o':
        return False
    while True:
        new_pos = Point(sand_position.x, sand_position.y + 1)
        if new_pos.y == len(field):
            return False
        if field[new_pos.y][new_pos.x] == '.':
            sand_position = new_pos
            continue
        new_pos = Point(sand_position.x - 1, sand_position.y + 1)
        if field[new_pos.y][new_pos.x] == '.':
            sand_position = new_pos
            continue
        new_pos = Point(sand_position.x + 1, sand_position.y + 1)
        if field[new_pos.y][new_pos.x] == '.':
            sand_position = new_pos
            continue
        break
    field[sand_position.y][sand_position.x] = 'o'
    return True

lines = open("../inputs/day_14.txt", "r").read().splitlines()
rock_paths = []
for line in lines:
    rock_paths.append(RockPath([list(map(int, position.split(","))) for position in line.split(" -> ")]))

min_x = min([path.min_x() for path in rock_paths])
max_x = max([path.max_x() for path in rock_paths])
min_y = 0
max_y = max([path.max_y() for path in rock_paths])

rock_points = set.union(*[path.path() for path in rock_paths])
sand_source = Point(500 - min_x + 1, 0)

# part I
field = [['.' for _ in range(max_x - min_x + 3) ] for _ in range(max_y - min_y + 2)]
for point in rock_points:
    field[point.y - min_y][point.x - min_x + 1] = '#'

field[sand_source.y][sand_source.x] = '+'


result = 0
while sand_move(field):
    result = result + 1

print(result)
# for row in field:
#     print(''.join(row))

# part II

height = max_y - min_y + 3
width = max_x - min_x + 2 * height
sand_source = Point(500 - min_x + height, 0)
field = [['.' for _ in range(width) ] for _ in range(height)]
for point in rock_points:
    field[point.y - min_y][point.x - min_x + height] = '#'

for idx, _ in enumerate(field[-1]):
    field[-1][idx] = '#'

field[sand_source.y][sand_source.x] = '+'

for row in field:
    print(''.join(row))

result = 0
while sand_move(field):
    result = result + 1

print(result)
for row in field:
    print(''.join(row))