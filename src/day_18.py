import itertools


def get_neighbors(x, y, z):
    return ((x - 1), y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)

class NeighborsCalculator:
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):
        self.min_x, self.max_x = min_x, max_x
        self.min_y, self.max_y = min_y, max_y
        self.min_z, self.max_z = min_z, max_z

    def get_neighbors(self, x, y, z):
        result = []
        if x - 1 >= self.min_x:
            result.append((x - 1, y, z))
        if x + 1 <= self.max_x:
            result.append((x + 1, y, z))
        if y - 1 >= self.min_y:
            result.append((x, y - 1, z))
        if y + 1 <= self.max_y:
            result.append((x, y + 1, z))
        if z - 1 >= self.min_z:
            result.append((x, y, z - 1))
        if z + 1 <= self.max_y:
            result.append((x, y, z + 1))
        return tuple(result)

lines = open("../inputs/day_18.txt", "r").read().splitlines()

lava_shape = set()
for line in lines:
    lava_shape.add(tuple(map(int, line.split(','))))

min_x = min(point[0] for point in lava_shape)
max_x = max(point[0] for point in lava_shape)

min_y = min(point[1] for point in lava_shape)
max_y = max(point[1] for point in lava_shape)

min_z = min(point[2] for point in lava_shape)
max_z = max(point[2] for point in lava_shape)

calculator = NeighborsCalculator(min_x, max_x, min_y, max_y, min_z, max_z)

# Part I
# result = sum([6 - len(lava_shape.intersection(set(get_neighbors(*point)))) for point in lava_shape])
# print(result) # 3498

part_one_result = sum([6 - len(lava_shape.intersection(set(calculator.get_neighbors(*point)))) for point in lava_shape])
print(part_one_result) # 3498

# result = sum([len(set(get_neighbors(*vortex)).difference(lava_shape)) for vortex in lava_shape])
# print(result) # 3498
# Part II

print(min_x, max_x, min_y, max_y, min_z, max_z)
print((max_x - min_x) * (max_y - min_y) * (max_z - min_z))

empty_surface_points = set(itertools.chain(*[
    list(itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1), [min_z])),
    list(itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1), [max_z])),
    list(itertools.product(range(min_x, max_x + 1), [min_y], range(min_z, max_z + 1))),
    list(itertools.product(range(min_x, max_x + 1), [max_y], range(min_z, max_z + 1))),
    list(itertools.product([min_x], range(min_y, max_y + 1), range(min_z, max_z + 1))),
    list(itertools.product([max_x], range(min_y, max_y + 1), range(min_z, max_z + 1)))
])).difference(lava_shape)

cube = {}
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        for z in range(min_z, max_z + 1):
            cube[(x, y, z)] = 0

for point in lava_shape:
    x, y, z = point
    cube[point] = 1

buffer = set(empty_surface_points)

while len(buffer) > 0:
    point = buffer.pop()
    cube[point] = 2
    neighbors = calculator.get_neighbors(*point)
    for item in set(neighbors).difference(lava_shape):
        if item not in buffer and cube[item] == 0:
            buffer.add(item)

spaces_inside = [k for k, v in cube.items() if v == 0]
need_to_subtract = sum([len(set(calculator.get_neighbors(*point)).difference(lava_shape)) for point in spaces_inside])

print(part_one_result - 6 * len(spaces_inside) + need_to_subtract)
