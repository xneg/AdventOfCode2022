import copy
import re
from collections import Counter
from itertools import groupby

pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. " \
          r"Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
lines = open("../inputs/day_19_test.txt", "r").read().splitlines()

blueprints = {}
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

initial_robots = Counter({"ore_robot": 1, "clay_robot": 0, "obsidian_robot": 0, "geode_robot": 0})
initial_minerals = Counter({"ore": 0, "clay": 0, "obsidian": 0, "geode": 0})
xxx(blueprints[1], initial_minerals, initial_robots, 0)
for result in results:
    print(result)

print(len(results))