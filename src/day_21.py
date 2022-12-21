import re

simple_pattern = r"([a-z]+): (-?\d+)"
math_pattern = r"([a-z]+): ([a-z]+) (.) ([a-z]+)"

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
    "*": lambda x, y: x * y,
}

class SimpleMonkey:
    def __init__(self, name, value):
        self.name = name
        self.value = int(value)

    def get_value(self, monkeys_dict):
        return self.value

class MathMonkey:
    def __init__(self, name, first, op, second):
        self.name = name
        self.first = first
        self.second = second
        self.op = op
        self.memoized_value = None

    def get_value(self, monkeys_dict):
        return ops[self.op](
                monkeys_dict[self.first].get_value(monkeys_dict),
                monkeys_dict[self.second].get_value(monkeys_dict))

regex_to_monkey = {
    simple_pattern: lambda match: SimpleMonkey(*match.groups()),
    math_pattern: lambda match: MathMonkey(*match.groups())
}

lines = open("../inputs/day_21.txt", "r").read().splitlines()

monkeys = {}
for line in lines:
    for (pattern, func) in regex_to_monkey.items():
        match = re.compile(pattern).match(line)
        if match is not None:
            monkey = func(match)
            monkeys[monkey.name] = monkey

# Part I
print("Part I", monkeys["root"].get_value(monkeys))

# Part II

monkeys["root"].op = '-'
monkeys["humn"].value = 1j
result = monkeys["root"].get_value(monkeys)

print("Part II", -result.real / result.imag)
