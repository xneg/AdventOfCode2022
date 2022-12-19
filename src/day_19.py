import re
from itertools import groupby
from operator import itemgetter

pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. " \
          r"Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
lines = open("../inputs/day_19.txt", "r").read().splitlines()

blueprints_array = []
for line in lines:
    blueprint, ore_robot, clay_robot, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian =\
        re.compile(pattern).match(line).groups()
    blueprints_array.append([
        (int(ore_robot), 0, 0, 0),
        (int(clay_robot), 0, 0, 0),
        (int(obsidian_robot_ore), int(obsidian_robot_clay), 0, 0),
        (int(geode_robot_ore), 0, int(geode_robot_obsidian), 0)])

def get_simple_purchases(minerals, blueprint):
    result = []
    for robot_idx, robot_price in enumerate(blueprint):
        remaining_minerals = [x - y for x, y in zip(minerals, robot_price)]
        if min(remaining_minerals) >= 0:
            result.append(([0 if i != robot_idx else 1 for i in range(4)], remaining_minerals))
    return result + [([0, 0, 0, 0], minerals)]

def get_greedy_purchases(minerals, blueprint):
    for robot_idx, robot_price in enumerate(reversed(blueprint)):
        remaining_minerals = [x - y for x, y in zip(minerals, robot_price)]
        if min(remaining_minerals) >= 0:
            return [([0 if i != robot_idx else 1 for i in range(4)], remaining_minerals)]
    return [([0, 0, 0, 0], minerals)]

def calculate(blueprint, initial_robots, initial_minerals, time_limit):
    results = []
    intermediate = set()

    def value_cost(remaining_time, robots, minerals):
        clay_cost = blueprint[1][0]
        obsidian_cost = blueprint[2][0] + blueprint[2][1] * clay_cost
        geode_cost = blueprint[3][0] + blueprint[3][2] * obsidian_cost
        return minerals[0] + minerals[1] * clay_cost + minerals[2] * obsidian_cost + minerals[3] * geode_cost + \
            (robots[0] + robots[1] * clay_cost + robots[2] * obsidian_cost + robots[3] * geode_cost) * remaining_time
    def calculate_step(blueprint, robots, minerals, time):
        if time >= time_limit:
            results.append((robots, minerals))
            return
        outcomes = get_simple_purchases(minerals, blueprint)
        # outcomes = get_greedy_purchases(minerals, blueprint)
        produced_minerals = robots
        for produced_robots, remaining_minerals in outcomes:
            new_robots = [x + y for x, y in zip(robots, produced_robots)]
            new_minerals = [x + y for x, y in zip(produced_minerals, remaining_minerals)]
            intermediate.add((time + 1, tuple(new_robots), tuple(new_minerals)))

    def pop(container, cond):
        try:
            value = next(filter(cond, container))
            container.remove(value)
            return value
        except StopIteration:
            raise Exception("No Value to pop")

    current_time = 0
    intermediate.add((0, tuple(initial_robots), tuple(initial_minerals)))
    while len(intermediate) > 0:
        min_time = min(k[0] for k in intermediate)
        if min_time != current_time:
            current_time = min_time
            intermediate = set(sorted(intermediate, key=lambda x: value_cost(time_limit - current_time, x[1], x[2]), reverse=True)[:1700])
        time, robots, minerals = pop(intermediate, lambda x: x[0] == min_time)
        calculate_step(blueprint, robots, minerals, time)
    return results

# print(10 * 33 * 47)
# for blueprint in blueprints_array[0:3]:
#     results = calculate(blueprint, [1, 0, 0, 0], [0, 0, 0, 0], 32)
#     bb = [(list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]
#     print(max([item[3] for sublist in bb for item in sublist]))

results = calculate(blueprints_array[10], [1, 0, 0, 0], [0, 0, 0, 0], 24) # 661
print(results)
bb = [(list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]
for b in bb:
    print(b)
print(max([item[3] for sublist in bb for item in sublist]))

exit()

total = 0
for idx, blueprint in enumerate(blueprints_array):
    results = calculate(blueprint, [1, 0, 0, 0], [0, 0, 0, 0], 24) # 661
    bb = [(list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]
    print(idx + 1, max([item[3] for sublist in bb for item in sublist]) * (idx + 1))
    total = total + max([item[3] for sublist in bb for item in sublist]) * (idx + 1)

print(total) # 1698 to low 1714 to low
exit()
1714