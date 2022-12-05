import re
from itertools import accumulate
from src.utils import chunker


def move_containers_9000(stack_from, stack_to, n):
    return stack_from[: len(stack_from) - n], stack_to + list(reversed(stack_from[-n:]))


def move_containers_9001(stack_from, stack_to, n):
    return stack_from[: len(stack_from) - n], stack_to + stack_from[-n:]

def changed_stacks(stacks, move_action, action):
    action_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    match = action_pattern.match(action)
    count, from_container, to_container = (
        int(match.groups()[0]),
        int(match.groups()[1]),
        int(match.groups()[2]),
    )
    new_from, new_to = move_action(stacks[from_container], stacks[to_container], count)
    return {**stacks, from_container: new_from, to_container: new_to}

lines = open("../inputs/day_5.txt", "r").read().splitlines()

containers = lines[0 : lines.index("")]
actions = lines[lines.index("") + 1 :]

container_pattern = re.compile(r"\[(.)]")
action_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

initial_stacks = {}
for row in list(reversed(containers))[1:]:
    idx = 1
    for el in list(chunker(row, 4)):
        match = container_pattern.match(el)
        if match:
            initial_stacks.setdefault(idx, [])
            initial_stacks[idx].append(match.groups()[0])
        idx = idx + 1

def func_part_one(stacks, action):
    return changed_stacks(stacks, move_containers_9000, action)

def func_part_two(stacks, action):
    return changed_stacks(stacks, move_containers_9001, action)

first_part = list(accumulate(actions, func_part_one, initial=initial_stacks))[-1]
print("".join(list(map(lambda x: x[-1], first_part.values()))))

second_part = list(accumulate(actions, func_part_two, initial=initial_stacks))[-1]
print("".join(list(map(lambda x: x[-1], second_part.values()))))
