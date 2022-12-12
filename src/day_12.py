class PriorityQueue:
    def __init__(self, queue):
        self.queue = queue

    def empty(self):
        return len(self.queue) == 0

    def add(self, element):
        self.queue.append(element)
        self.queue = sorted(self.queue, key=lambda x: x[1], reverse=True)

    def pop(self):
        value, priority = self.queue.pop()
        return value

def comparison_part_one(current, neighbor):
    return neighbor - current > 1

def comparison_part_two(current, neighbor):
    return current > neighbor + 1

def neighbors(current, field, comparison_func):
    result = []
    current_height = field[current[0]][current[1]]
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
        node_position = (current[0] + new_position[0], current[1] + new_position[1])

        if node_position[0] > (len(field) - 1) or node_position[0] < 0 or node_position[1] > (
                len(field[len(field) - 1]) - 1) or node_position[1] < 0:
            continue
        neighbor_height = field[node_position[0]][node_position[1]]
        if comparison_func(current_height, neighbor_height):
            continue
        result.append(node_position)
    return result
def dijkstra_search(field, start, goal_func, comparison_func):
    frontier = PriorityQueue([(start, 0)])
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.pop()

        if goal_func(current):
            break

        for next in neighbors(current, field, comparison_func):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.add((next, priority))
                came_from[next] = current

    return came_from, cost_so_far

lines = open("../inputs/day_12.txt", "r").read().splitlines()

field = []
for line in lines:
    field.append([ord(c) for c in line])

start = [(idx, row.index(ord('S'))) for idx, row in enumerate(field) if ord('S') in row][0]
end =   [(idx, row.index(ord('E'))) for idx, row in enumerate(field) if ord('E') in row][0]

field[start[0]][start[1]] = ord('a')
field[end[0]][end[1]] = ord('z')

path_one = dijkstra_search(field, start, lambda x: x == end, comparison_part_one)
print(path_one[1][end])

path_two = dijkstra_search(field, end, lambda x: field[x[0]][x[1]] == ord('a'), comparison_part_two)
print(min({value for key, value in path_two[1].items() if field[key[0]][key[1]] == ord('a')}))
