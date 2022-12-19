import copy
import re
from collections import Counter
from itertools import groupby
from operator import itemgetter

pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. " \
          r"Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
lines = open("../inputs/day_19_test.txt", "r").read().splitlines()

blueprints = {}
blueprints_array = []
for line in lines:
    blueprint, ore_robot, clay_robot, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian =\
        re.compile(pattern).match(line).groups()
    blueprints[int(blueprint)] = {
        "ore_robot": {"ore": int(ore_robot)},
        "clay_robot": {"ore": int(clay_robot)},
        "obsidian_robot": {
            "ore": int(obsidian_robot_ore),
            "clay": int(obsidian_robot_clay),
        },
        "geode_robot": {
            "ore": int(geode_robot_ore),
            "obsidian": int(geode_robot_obsidian)
        }
    }
    blueprints_array.append([
        (int(ore_robot), 0, 0, 0),
        (int(clay_robot), 0, 0, 0),
        (int(obsidian_robot_ore), int(obsidian_robot_clay), 0, 0),
        (int(geode_robot_ore), 0, int(geode_robot_obsidian), 0)])

# print(blueprints)

time_limit = 24
current_time = 0

initial_minerals = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
initial_robots = {"ore_robot": 1, "clay_robot": 0, "obsidian_robot": 0, "geode_robot": 0}

def get_all_outcomes(initial_minerals, blueprint):
    combo = []
    def get_all_possible_purchases(minerals, blueprint, acc):
        for robot, price in blueprint.items():
            purchasable = True
            current_minerals = copy.deepcopy(minerals)
            for (mineral, cost) in price.items():
                if current_minerals[mineral] < cost:
                    purchasable = False
                    break
                else:
                    current_minerals[mineral] = current_minerals[mineral] - cost
            if purchasable:
                current_combo = [(key, len(list(group))) for key, group in groupby(sorted(acc + [robot]))]
                combo.append((current_combo, current_minerals))
                get_all_possible_purchases(current_minerals, blueprint, acc + [robot])

    get_all_possible_purchases(minerals = initial_minerals, blueprint=blueprint, acc=[])
    return combo + [([], initial_minerals)]


def produce_minerals(robots):
    robot_mineral_map = {"ore_robot": "ore", "clay_robot": "clay", "obsidian_robot": "obsidian", "geode_robot": "geode"}
    return Counter({robot_mineral_map[robot]: count for robot, count in robots.items()})


results = []
def xxx(blueprint, minerals, robots, time):
    if time > 15:
        results.append((minerals, robots))
        return
    outcomes = get_all_outcomes(initial_minerals=minerals, blueprint=blueprint)
    produced_minerals = produce_minerals(robots)
    for new_robots, remaining_minerals in outcomes:
        current_robots = copy.deepcopy(robots)
        for robot, count in new_robots:
            current_robots[robot] = current_robots[robot] + count
        xxx(blueprint, produced_minerals + remaining_minerals, current_robots, time + 1)

# initial_robots = Counter({"ore_robot": 1, "clay_robot": 0, "obsidian_robot": 0, "geode_robot": 0})
# initial_minerals = Counter({"ore": 0, "clay": 0, "obsidian": 0, "geode": 0})
# xxx(blueprints[1], initial_minerals, initial_robots, 0)
# for result in results:
#     print(result)
#
# print(len(results))
# print(blueprints_array[0])
# exit()

def get_outcomes_array(initial_minerals, blueprint):
    combo = []
    def get_all_possible_purchases(minerals, blueprint, acc):
        for robot_idx, robot_price in enumerate(blueprint):
            purchasable = True
            for mineral_idx, cost in enumerate(robot_price[:-1]):
                if minerals[mineral_idx] < cost:
                    purchasable = False
                    break
            if purchasable:
                new_acc = acc[0:robot_idx] + [acc[robot_idx] + 1] + acc[robot_idx+1:]
                remaining_minerals = [x - y for x, y in zip(minerals, robot_price)]
                combo.append((new_acc, remaining_minerals))
                get_all_possible_purchases(remaining_minerals, blueprint, new_acc)

    get_all_possible_purchases(minerals = initial_minerals, blueprint=blueprint, acc=[0, 0, 0, 0])
    return combo + [([0, 0, 0, 0], initial_minerals)]


def get_simple_purchases(minerals, blueprint):
    result = []
    for robot_idx, robot_price in enumerate(blueprint):
        remaining_minerals = [x - y for x, y in zip(minerals, robot_price)]
        if min(remaining_minerals) >= 0:
            result.append(([0 if i != robot_idx else 1 for i in range(4)], remaining_minerals))
    return result + [([0, 0, 0, 0], minerals)]

def calculate(blueprint, initial_robots, initial_minerals, time_limit):
    results = []
    intermediate = set()

    def calculate_value(remaining_time, robots, minerals):
        # return x[0] * 4 + y[0] + x[1] * 2 + y[1] * 2 + x[2] * 11 + y[2] * 11 + x[3] * 1000
        # return x[0] * 10 + y[0] + x[1] * 100 + y[1] * 10 + x[2] * 1000 + y[2] * 100 + x[3] * 100000

        # Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        return minerals[0] + 2 * minerals[1] + 31 * minerals[2] + (2 + 7 * 31) * minerals[3] + \
            (robots[0] + 2 * robots[1] + 31 * robots[2] + (2 + 7 * 31) *robots[3]) * remaining_time

        # Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
        # return minerals[0] + 3 * minerals[1] + (3 + 8 * 3) * minerals[2] + (3 + 12 * (3 + 8 * 3)) * minerals[3] + \
        #     (robots[0] + 3 * robots[1] + (3 + 8 * 3) * robots[2] + (3 + 12 * (3 + 8 * 3)) * robots[3]) * remaining_time
    def calculate_step(blueprint, robots, minerals, time):
        if time >= time_limit:
            results.append((robots, minerals))
            return
        outcomes = get_simple_purchases(minerals, blueprint)
        produced_minerals = robots
        # outcomes = sorted(outcomes, key=lambda x: calculate_value(time_limit = time, *x), reverse=True)#[:5]
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

    import time
    current_time = 0
    intermediate.add((0, tuple(initial_robots), tuple(initial_minerals)))
    while len(intermediate) > 0:
        min_time = min(k[0] for k in intermediate)
        if min_time != current_time:
            current_time = min_time
            # intermediate = set(sorted(intermediate, key=lambda x: calculate_value(x[1], x[2]), reverse=True))
            # intermediate = set(sorted(intermediate, key=lambda x: calculate_value(time_limit - current_time, x[1], x[2]), reverse=True)[:100])
            # bb = [(k, list(list(zip(*g))[2])) for k, g in groupby(sorted(intermediate), itemgetter(1))]
            # print("bb", min_time)
            # for b in bb:
            #     print(b)
        time, robots, minerals = pop(intermediate, lambda x: x[0] == min_time) #intermediate.pop()
        # print(time)
        calculate_step(blueprint, robots, minerals, time)
    return results

# print(calculate(blueprints_array[0], [1, 0, 0, 0], [0, 0, 0, 0], 6))
# exit()

# 18 - 164
# Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
results = calculate(blueprints_array[0], [1, 0, 0, 0], [0, 0, 0, 0], 15) # 661
print(results)
# current_combo = [(key, len(list(group))) for key, group in groupby(sorted(acc + [robot]))]
# b = [(k, list(list(zip(*g))[1])) for k, g in groupby(a, itemgetter(0))]
# print(results)
# print(len(results))
# print(results)
# bb = [(k, list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]
bb = [(list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]

print(max([item[3] for sublist in bb for item in sublist]))
# for b in bb:
#     print(b)
# print(len(bb))
# print [list(g[1]) for g in groupby(sorted(results, key=len), len)]