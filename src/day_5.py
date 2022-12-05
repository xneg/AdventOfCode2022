import re
import copy
from src.utils import chunker


def move_containers_9000(stack_from, stack_to, n):
    return stack_from[: len(stack_from) - n], stack_to + list(reversed(stack_from[-n:]))


def move_containers_9001(stack_from, stack_to, n):
    return stack_from[: len(stack_from) - n], stack_to + stack_from[-n:]


lines = open("../inputs/day_5.txt", "r").read().splitlines()

containers = lines[0 : lines.index("")]
actions = lines[lines.index("") + 1 :]

container_pattern = re.compile(r"\[(.)]")
action_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

stacks = {}
for row in list(reversed(containers))[1:]:
    idx = 1
    for el in list(chunker(row, 4)):
        match = container_pattern.match(el)
        if match:
            stacks.setdefault(idx, [])
            stacks[idx].append(match.groups()[0])
        idx = idx + 1

stacks_first_part = copy.deepcopy(stacks)
stacks_second_part = copy.deepcopy(stacks)

for action in actions:
    match = action_pattern.match(action)
    count, from_container, to_container = (
        int(match.groups()[0]),
        int(match.groups()[1]),
        int(match.groups()[2]),
    )
    (
        stacks_first_part[from_container],
        stacks_first_part[to_container],
    ) = move_containers_9000(
        stacks_first_part[from_container], stacks_first_part[to_container], count
    )

    (
        stacks_second_part[from_container],
        stacks_second_part[to_container],
    ) = move_containers_9001(
        stacks_second_part[from_container], stacks_second_part[to_container], count
    )

print("".join(list(map(lambda x: x[-1], stacks_first_part.values()))))
print("".join(list(map(lambda x: x[-1], stacks_second_part.values()))))
