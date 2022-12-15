import re

pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
class Sensor:
    x_min = 0
    x_max = 4000000
    y_min = 0
    y_max = 4000000
    def __init__(self, x, y, nearest_beacon_x, nearest_beacon_y):
        self.x = int(x)
        self.y = int(y)
        self.beacon_x = int(nearest_beacon_x)
        self.beacon_y = int(nearest_beacon_y)

    def get_result_part_one(self, y_of_interest):
        manhattan_distance = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)
        x_half_range = manhattan_distance - abs(self.y - y_of_interest)
        result = (None, None)
        if x_half_range > 0:
            result = list(range(max(Sensor.x_min, self.x - x_half_range), min(Sensor.x_max, self.x + x_half_range + 1)))
            # if self.beacon_y == y_of_interest:
            #     result.remove(self.beacon_x)
        return result

    def get_result_part_two(self, y_of_interest):
        manhattan_distance = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)
        x_half_range = manhattan_distance - abs(self.y - y_of_interest)
        result = (None, None)
        if x_half_range > 0:
            result = max(Sensor.x_min, self.x - x_half_range), min(Sensor.x_max, self.x + x_half_range)
        return result

    def get_empty_spaces(self):
        result = set()
        manhattan_distance = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)
        left = max(Sensor.x_min, self.x - manhattan_distance)
        right = min(Sensor.x_max, self.x + manhattan_distance)
        for i in range(left, right + 1):
            up = max(Sensor.y_min, self.y + abs(self.x - i) - manhattan_distance)
            down = min(Sensor.y_max, self.y - abs(self.x - i) + manhattan_distance)
            for j in range(up, down + 1):
                result.add((i, j))
        return result

    def check_in_reach(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)


lines = open("../inputs/day_15_test.txt", "r").read().splitlines()

sensors = [Sensor(*pattern.match(line).groups()) for line in lines]

# Sensor.x_max = 20


def row_detection(sensors, y, x_max):
    global results
    results = list(zip(*[sensor.get_result_part_two(y) for sensor in sensors]))
    b_iter = iter(sorted(results[0], key=lambda x: (x is None, x)))
    e_iter = iter(sorted(results[1], key=lambda x: (x is None, x)))
    # print(sorted(results[0], key=lambda x: (x is None, x)))
    # print(sorted(results[1], key=lambda x: (x is None, x)))

    b = next(b_iter)
    e = next(e_iter)
    intervals = 0
    while b is not None:
        if b < e + 1:
            intervals = intervals + 1
            b = next(b_iter)
        elif b == e + 1:
            b = next(b_iter)
            e = next(e_iter)
        else:
            intervals = intervals - 1
            if intervals == 0:
                break
            e = next(e_iter)

        if e == x_max + 1:
            break
    return intervals, e + 1

# for i in range(0, 21):
#     intervals, _ = row_detection(i, 20)
#     if intervals == 0:
#         print(i)

lines = open("../inputs/day_15.txt", "r").read().splitlines()

sensors = [Sensor(*pattern.match(line).groups()) for line in lines]

import time
start_time = time.time()
Sensor.x_max = 4000000
for i in range(0, 2000001):
    intervals, x = row_detection(sensors, 2000001 + i, 4000000)
    if intervals == 0:
        print(x, 2000001 + i)
        break
    intervals, x = row_detection(sensors, 2000000 - i, 4000000)
    if intervals == 0:
        print(x, 2000000 - i)
        break
print("--- %s seconds ---" % (time.time() - start_time))


# Part I
# line_of_interest = 2000000
# results = [sensor.get_result_part_one(line_of_interest) for sensor in sensors]
# print(len(set(sum(results, [])))) #32

# Part II
x = 3138881
y = 3364986
# print(row_detection(sensors, y, 4000000))
print(x * 4000000 + y)
# results = [sensor.get_empty_spaces() for sensor in sensors]
# result_6 = sensors[6].get_empty_spaces()

for i in range(x-3, x+3):
    for j in range(y-3, y+3):
        in_reach = False
        for sensor in sensors:
            if sensor.check_in_reach(i, j):
                in_reach = True
                break
        if not in_reach:
            print(i, j)
# 12555523364986
