import re
from itertools import groupby

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
time_limit = 30
current_time = 0
opened_valves = []

solution_space = []

distances = {}
for valve in valuable_valves:
    distances[("AA", valve)], _ = printShortestDistance(adj, valves_to_ints["AA"], valves_to_ints[valve], graph_length)
    distances[(valve, "AA")], _ = printShortestDistance(adj, valves_to_ints["AA"], valves_to_ints[valve], graph_length)
    for other_valve in [v for v in valuable_valves if v != valve]:
        distances[(valve, other_valve)], _ = printShortestDistance(adj, valves_to_ints[valve], valves_to_ints[other_valve], graph_length)

def solve(current, available, current_time, path):
    if len(available) == 0 or current_time == 30:
        solution_space.append(path + [current])
        return

    for valve in available:
        dist = distances[(current, valve)]
        time = current_time + dist + 1
        if time <= 30:
            solve(valve, [a for a in available if a != valve], time, path + [current])

    solution_space.append(path + [current])

solve("AA", valuable_valves, 0, [])
total = 0
print(len(solution_space)) #86593
for solution in solution_space:
    result = 0
    time = 0
    for idx, point in enumerate(solution[1:]):
        dist = distances[point, solution[idx]]
        time = time + dist + 1
        pressure = valves_dict[point].pressure_produce(time, time_limit)
        result = result + valves_dict[point].pressure_produce(time, time_limit)
    if result > total:
        total = result
print(total)
exit()

# 1572 ['AA', 'MD', 'DS', 'FS', 'HG', 'PZ', 'JE', 'YB', 'IT'] 34
# 1574 ['AA', 'MD', 'DS', 'YW', 'FS', 'HG', 'PZ', 'JE', 'IK'] 30
# 1580 ['AA', 'MD', 'DS', 'FS', 'HG', 'PZ', 'JE', 'YB'] 28