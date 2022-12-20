from src.utils import sign


class Node:
    def __init__(self, value, prev, next):
        self.value = value
        self.prev = prev
        self.next = next
        self.is_beginning = False

lines = open("../inputs/day_20.txt", "r").read().splitlines()
secret_number = 811589153
input = [secret_number * int(line) for line in lines]

prev = None
initial = None
nodes = []
for el in input:
    current = Node(el, prev, None)
    nodes.append(current)
    if prev is not None:
        prev.next = current
    else:
        initial = current
    prev = current

prev.next = initial
initial.prev = prev
initial.is_beginning = True

print([node.value for node in nodes])

for i in range(10):
    for node_idx, node in enumerate(nodes):
        periods_count = abs(node.value) // (len(nodes) - 1)
        move_steps = sign(node.value) * (abs(node.value) - (periods_count - 1) * (len(nodes) - 1))
        if move_steps == 0:
            continue
        left = node.prev
        right = node.next
        left.next = right
        right.prev = left

        x = node
        for i in range(abs(move_steps)):
            if node.value > 0:
                x = x.next
            else: x = x.prev

        if move_steps >= 0:
            left = x
            right = x.next
        else:
            left = x.prev
            right = x

        left.next = node
        right.prev = node
        node.prev = left
        node.next = right

result = []
start = [node for node in nodes if node.value == 0][0]
result.append(start.value)
next = start.next
while next != start:
    result.append(next.value)
    next = next.next

# print(result)
# exit()

idx1 = (1000 % len(result) + result.index(0)) % len(result)
idx2 = (2000 % len(result) + result.index(0)) % len(result)
idx3 = (3000 % len(result) + result.index(0)) % len(result)

print(result[idx1], result[idx2], result[idx3])
print(result[idx1] + result[idx2] + result[idx3])
