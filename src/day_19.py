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

def calculate(blueprint, initial_robots, initial_minerals, time_limit):
    results = []
    intermediate = {}

    def calculate_value(robots, minerals):
        return [x*10 + y for x, y in zip(robots, minerals)]
        # return minerals[0] + minerals[1]*10 + minerals[2]*100 + minerals[3]*1000
    def calculate_step(blueprint, robots, minerals, time):
        if time >= time_limit:
            results.append((robots, minerals))
            return
        outcomes = get_outcomes_array(initial_minerals=minerals, blueprint=blueprint)
        produced_minerals = robots
        outcomes = sorted(outcomes, key=lambda x: calculate_value(*x), reverse=True)[:5]
        for produced_robots, remaining_minerals in outcomes:
            new_robots = [x + y for x, y in zip(robots, produced_robots)]
            new_minerals = [x + y for x, y in zip(produced_minerals, remaining_minerals)]
            add_intermidiate(time + 1, new_robots, new_minerals)

    import time
    def add_intermidiate(time, robots, minerals):
        if (time, tuple(robots)) not in intermediate:
            intermediate[(time, tuple(robots))] = set([tuple(minerals)])
        else:
            intermediate[(time, tuple(robots))].add(tuple(minerals))

    intermediate[(0, tuple(initial_robots))] = set([tuple(initial_minerals)])
    while len(intermediate) > 0:
        print(len(intermediate))
        min_time = min(k[0] for k in intermediate.keys())
        key, value = [(key, value) for key, value in intermediate.items() if key[0] == min_time][0]
        del intermediate[key]

        my_time, robots = key
        most_vectors = []
        for item in value:
            need_add = True
            for other in value:
                if item != other and max([x - y for x, y in zip(item, other)]) <= 0:
                    need_add = False
                    break
            if need_add:
                most_vectors.append(item)

        for minerals in most_vectors:
            calculate_step(blueprint, robots, minerals, my_time)
    return results

# print(calculate(blueprints_array[0], [1, 0, 0, 0], [0, 0, 0, 0], 6))
# exit()

# 18 - 164
results = calculate(blueprints_array[0], [1, 0, 0, 0], [0, 0, 0, 0], 20) # 661
# current_combo = [(key, len(list(group))) for key, group in groupby(sorted(acc + [robot]))]
# b = [(k, list(list(zip(*g))[1])) for k, g in groupby(a, itemgetter(0))]
# print(results)
print(len(results))
bb = [(k, list(list(zip(*g))[1])) for k, g in groupby(sorted(results), itemgetter(0))]
for b in bb:
    print(b)
print(len(bb))
# print [list(g[1]) for g in groupby(sorted(results, key=len), len)]