import re

from src.utils import printShortestDistance


class Valve:
    def __init__(self, name, pressure, neighbors):
        self.name = name
        self.pressure = int(pressure)
        self.neighbors = neighbors.split(", ")

    def pressure_produce(self, start, end):
        return (end - start) * self.pressure

pattern = re.compile(r"Valve ([A-Z]{2}.*) has flow rate=(-?\d+); tunnels?\b leads?\b to valves?\b (.*)")

lines = open("../inputs/day_16.txt", "r").read().splitlines()

valves = [Valve(*pattern.match(line).groups()) for line in lines]
valves_dict = {valve.name: valve for valve in valves}

# prepare for using the shortest path
valves_to_ints = {key: index for index, key in enumerate(valves_dict)}
ints_to_valves = {index: key for index, key in enumerate(valves_dict)}
graph_length = len(valves_dict)
adj = [[] for i in range(graph_length)]
for index, key in enumerate(valves_dict):
    adj[index] = [valves_to_ints[n] for n in valves_dict[key].neighbors]

valuable_valves = [valve.name for valve in valves_dict.values() if valve.pressure > 0]

current = "AA"

solution_space = []

distances = {}
for valve in valuable_valves:
    distances[("AA", valve)], _ = printShortestDistance(adj, valves_to_ints["AA"], valves_to_ints[valve], graph_length)
    distances[(valve, "AA")], _ = printShortestDistance(adj, valves_to_ints["AA"], valves_to_ints[valve], graph_length)
    for other_valve in [v for v in valuable_valves if v != valve]:
        distances[(valve, other_valve)], _ = printShortestDistance(adj, valves_to_ints[valve], valves_to_ints[other_valve], graph_length)

def solve(current, available, current_time, path, time_limit):
    solution_space.append(tuple(path + [current]))
    if len(available) == 0 or current_time == time_limit:
        return

    for valve in available:
        dist = distances[(current, valve)]
        time = current_time + dist + 1
        if time <= time_limit:
            solve(valve, [a for a in available if a != valve], time, path + [current], time_limit)

def calc_total(solution, time_limit):
    result = 0
    time = 0
    for idx, point in enumerate(solution[1:]):
        dist = distances[point, solution[idx]]
        time = time + dist + 1
        result = result + valves_dict[point].pressure_produce(time, time_limit)
    return result

solve("AA", valuable_valves, 0, [], 30)
total = 0
print(len(solution_space)) #86593
print(max([calc_total(solution, 30) for solution in solution_space]))

# Part II
solution_space = []
solve("AA", valuable_valves, 0, [], 26)
print("solution space 2", len(solution_space))

solution_space = sorted(solution_space, key=lambda x: calc_total(x, 26), reverse=True)[:400]
print("solution space 2 reduced", len(solution_space))

total = 0
for my_idx, my in enumerate(solution_space):
    for el_idx in range(my_idx+1, len(solution_space)):
        el = solution_space[el_idx]
        my_set = set(my)
        el_set = set(el)
        intersection = set.intersection(my_set, el_set)
        if len(intersection) == 1:
            result = calc_total(my, 26) + calc_total(el, 26)
            if result > total: total = result

print("total", total) #2213
