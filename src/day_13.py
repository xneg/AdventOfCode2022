import ast
import itertools
from functools import cmp_to_key
from src.utils import chunker
def compare(left, right):
    if left is None:
        return 1
    if right is None:
        return -1
    if not isinstance(left, list) and not isinstance(right, list):
        if left < right:
            return 1
        elif left > right:
            return -1
        return 0

    if not isinstance(left, list): left = [left]
    if not isinstance(right, list): right = [right]

    if isinstance(left, list) and isinstance(right, list):
        my_zip = list(itertools.zip_longest(left, right))
        result = 0
        for l, r in my_zip:
            result = compare(l, r)
            if result != 0: return result
        return result

lines = open("../inputs/day_13.txt", "r").read().splitlines()
result = 0
for idx, pair in enumerate(chunker(lines, 3)):
    if compare(ast.literal_eval(pair[0]), ast.literal_eval(pair[1])) == 1:
        result = result + idx + 1

print(result)

signals = []
for pair in chunker([line for line in lines if len(line) > 0], 2):
    signals.extend([ast.literal_eval(s) for s in pair[:2]])

divider_packets = [[[2]], [[6]]]
signals.extend(divider_packets)

signals = sorted(signals, key=cmp_to_key(compare), reverse=True)

print((signals.index(divider_packets[0]) + 1) * (signals.index(divider_packets[1]) + 1))