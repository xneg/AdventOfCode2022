import ast
import itertools
from functools import cmp_to_key
from src.utils import chunker

def compare(left, right):
    if not isinstance(left, list) and not isinstance(right, list):
        if left < right:
            return 1
        elif left > right:
            return -1
        return 0

    if not isinstance(left, list): left = [left]
    if not isinstance(right, list): right = [right]

    result = 0
    for l, r in list(itertools.zip_longest(left, right, fillvalue=-1)):
        result = compare(l, r)
        if result != 0: return result
    return result

lines = open("../inputs/day_13.txt", "r").read().splitlines()
signals = []
for pair in chunker([line for line in lines if len(line) > 0], 2):
    signals.extend([ast.literal_eval(s) for s in pair[:2]])

#first part

result = sum([idx + 1 for idx, pair in enumerate(chunker(signals, 2))
              if compare(pair[0], pair[1]) == 1])
print(result)

# second part
divider_packets = [[[2]], [[6]]]
signals.extend(divider_packets)

signals = sorted(signals, key=cmp_to_key(compare), reverse=True)

print((signals.index(divider_packets[0]) + 1) * (signals.index(divider_packets[1]) + 1))