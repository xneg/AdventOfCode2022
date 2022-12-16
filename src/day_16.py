import re

class Valve:
    def __init__(self, name, pressure, others):
        self.name = name
        self.pressure = int(pressure)
        self.others = others.split(",")

pattern = re.compile(r"Valve ([A-Z]{2}.*) has flow rate=(-?\d+); tunnels?\b leads?\b to valves?\b (.*)")

lines = open("../inputs/day_16_test.txt", "r").read().splitlines()

valves = [Valve(*pattern.match(line).groups()) for line in lines]

for valve in valves:
    print(valve.name, valve.pressure, valve.others)



