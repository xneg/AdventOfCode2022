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

    def get_accum(self, accum_func, accum):
        total = 0
        for c in self.children.values():
            result, accum = c.get_accum(accum_func, accum)
            total = total + result
        total = total + self.size
        return total, accum_func(accum, total, is_dir = len(self.children) > 0)

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

patterns={r"\$ ls": ls, r"dir (.+)": dir, r"\$ cd (.+)": cd, r"(\d+) (.+)": file}

lines = open("../inputs/day_7.txt", "r").read().splitlines()
current_node = Node(None, "/", 0)
for line in lines[1:]:
    for pattern, case in patterns.items():
        match = re.compile(pattern).match(line)
        current_node = case(match, current_node)

while current_node.parent is not None:
    current_node = current_node.parent

def first_part(accum, total, is_dir):
    return accum + total if total <= 100000 and is_dir else accum

total_size, accum = current_node.get_accum(accum_func=first_part, accum=0)
print(accum)

total_disc_space = 70000000
space_for_update = 30000000

free_space = total_disc_space - total_size
need_to_free = space_for_update - free_space

def second_part(accum, total, is_dir):
    return total if is_dir and need_to_free < total < accum else accum

total_size, accum2 = current_node.get_accum(accum_func=second_part, accum=total_disc_space)
print(accum2)


input = "dfsfdfdf"

switch (input):
    case regex1:
        temp = ...
    case regex2:
        temp = ...