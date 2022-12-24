from src.utils import PriorityQueue


class Blizzard:
    direction_map = {
        ">": (1, 0),
        "<": (-1, 0),
        "^": (0, -1),
        "v": (0, 1)
    }
    field_height = None
    field_width = None
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.direction = Blizzard.direction_map[direction]

    def move(self, time):
        x = (self.x + self.direction[0] * time) % Blizzard.field_width
        y = (self.y + self.direction[1] * time) % Blizzard.field_height
        return x, y

def dijkstra_search(start, goal_func, neighbors_func):
    frontier = PriorityQueue([(start, 0)])
    came_from = {}
    cost_so_far = {start: 0}
    came_from[start] = None

    while len(frontier.queue) > 0:
        current = frontier.pop()

        if goal_func(current):
            break

        for next in neighbors_func(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.add((next, priority))
                came_from[next] = current
    return came_from, cost_so_far

lines = open("../inputs/day_24.txt", "r").read().splitlines()

Blizzard.field_height = len(lines) - 2
Blizzard.field_width = len(lines[0]) - 2
blizzards = []
for y, line in enumerate(lines[1:-1]):
    for x, cell in enumerate(line[1:-1]):
        if cell != '.':
            blizzards.append(Blizzard(x=x, y=y, direction=cell))

initial_point = (lines[0].index('.') - 1, -1)
final_point = (lines[-1].index('.') - 1, len(lines) - 2)
print("initial", initial_point, "final", final_point)

planes = {}
def fill_planes(time):
    planes[time] = {blizzard.move(time) for blizzard in blizzards}
def neighbors_func(current):
    x, y, current_time = current
    next_time = current_time + 1
    if next_time not in planes:
        fill_planes(next_time)

    result = []
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:  # Adjacent squares
        new_position = (x + direction[0], y + direction[1])
        if new_position != final_point and new_position != initial_point:
            if new_position[0] < 0 or new_position[0] > Blizzard.field_width - 1 or new_position[1] < 0 \
                or new_position[1] > Blizzard.field_height - 1 or new_position in planes[next_time]:
                    continue
        result.append(tuple([*new_position, next_time]))
    return result


# Part I
result = dijkstra_search(tuple([*initial_point, 0]), lambda x: (x[0], x[1]) == final_point, neighbors_func)
there_first = [point for point in result[1] if (point[0], point[1]) == final_point][0]
print(there_first)
# Part II
back_result = dijkstra_search(there_first, lambda x: (x[0], x[1]) == initial_point, neighbors_func)
back = [point for point in back_result[1] if (point[0], point[1]) == initial_point][0]
result_two = dijkstra_search(back, lambda x: (x[0], x[1]) == final_point, neighbors_func)
there_second = [point for point in result_two[1] if (point[0], point[1]) == final_point][0]
print(there_second)