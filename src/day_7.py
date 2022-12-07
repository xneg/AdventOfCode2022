import re
from typing import Dict


class Node:
    def __init__(self, parent: "Node", name: str, size: int):
        self.parent = parent
        self.name = name
        self.size = size
        self.children: Dict[str, "Node"] = {}

    def add_child(self, child: "Node"):
        self.children[child.name] = child

    def total_size(self):
        result = 0
        for c in self.children.values():
            result = result + c.total_size()
        total = result + self.size
        self.total = total
        return total

    def print(self, level):
        type = 'dir' if len(self.children) > 0 else 'file'
        print(' ' * level + f"- {self.name} ({type}) {self.total_size()}")
        for c in self.children.values():
            c.print(level + 1)

    def total_size_accum(self, accum):
        total = 0
        for c in self.children.values():
            result, accum = c.total_size_accum(accum)
            total = total + result
        total = total + self.size
        if total <= 100000 and len(self.children.values()) > 0:
            accum.append(total)
        return total, accum

    def total_size_accum_2(self, accum):
        total = 0
        for c in self.children.values():
            result, accum = c.total_size_accum_2(accum)
            total = total + result
        total = total + self.size
        if len(self.children.values()) > 0 and 2805968 < total < accum:
            accum = total
        return total, accum

def ls(match, current_node):
    return current_node

def dir(match, current_node: Node):
    if match:
        name = match.groups()[0]
        new_node = Node(parent=current_node, name = name, size=0)
        current_node.add_child(new_node)
    return current_node

def cd(match, current_node: Node):
    if match:
        dest = match.groups()[0]
        if dest == "..":
            return current_node.parent
        else:
            return current_node.children[dest]
    return current_node

def file(match, current_node: Node):
    if match:
        size, name = match.groups()[0], match.groups()[1]
        new_node = Node(parent=current_node, name=name, size=int(size))
        current_node.add_child(new_node)
    return current_node

patterns=[r"\$ ls", r"dir (.+)", r"\$ cd (.+)", r"(\d+) (.+)"]
functions=[ls, dir, cd, file]

lines = open("../inputs/day_7.txt", "r").read().splitlines()
current_node = Node(None, "/", 0)
for line in lines[1:]:
    for pattern, case in zip(patterns, functions):
        match = re.compile(pattern).match(line)
        current_node = case(match, current_node)

while current_node.parent is not None:
    current_node = current_node.parent

print(current_node.total_size()) #48381165

# current_node.print(0)
total_size, accum = current_node.total_size_accum([])
print(accum)
print(sum(accum))

total_disc_space = 70000000
space_for_update = 30000000

free_space = total_disc_space - current_node.total_size()
need_to_free = space_for_update - free_space
print(need_to_free)
total, accum2 = current_node.total_size_accum_2(total_disc_space)
print(accum2)