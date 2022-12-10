import re

from src.utils import chunker

points_of_interest = [20, 60, 100, 140, 180, 220]

def noop(_, cycle, value):
    return cycle + 1, value, [value]

def addx(match, cycle, value):
    return cycle + 2, value + int(match.groups()[0]), [value, value]

ops = {r"noop": noop, r"addx (-?\d+)": addx}

lines = open("../inputs/day_10.txt", "r").read().splitlines()

cycle = 0
x = 1
result = []
for line in lines:
    for pattern, case in ops.items():
        match = re.compile(pattern).match(line)
        if match:
            cycle, x, addition = case(match, cycle, x)
            result.extend(addition)

print(sum([result[point-1] * point for point in points_of_interest]))

for line in chunker(result, 40):
    print(*['#' if abs(idx - register) < 2 else '.' for idx, register in enumerate(line)])