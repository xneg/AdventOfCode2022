from typing import List
limit = 23 * 19 * 13 * 17 # test
limit = 13 * 19 * 5 * 2 * 17 * 11 * 7 * 3
class Monkey:
    def __init__(self, starting_items, op, test):
        self.monkeys = None
        self.items = starting_items
        self.op = op
        self.test = test
        self.total_expected = 0

    def set_all_monkeys(self, monkeys):
        self.monkeys = monkeys

    def act(self):
        for item in self.items:
            self.total_expected = self.total_expected + 1
            item = self.op(item) # // 3
            sub = item // limit
            item = item - limit * sub
            next_monkey = self.test(item)
            self.monkeys[next_monkey].items.append(item)
        self.items = []



# test monkeys
# monkeys = [
#     Monkey(starting_items=[79, 98], op=(lambda x: x * 19), test=(lambda x: 2 if x % 23 == 0 else 3)),
#     Monkey(starting_items=[54, 65, 75, 74], op=(lambda x: x + 6), test=(lambda x: 2 if x % 19 == 0 else 0)),
#     Monkey(starting_items=[79, 60, 97], op=(lambda x: x * x), test=(lambda x: 1 if x % 13 == 0 else 3)),
#     Monkey(starting_items=[74], op=(lambda x: x + 3), test=(lambda x: 0 if x % 17 == 0 else 1))]

monkeys = [
    Monkey(starting_items=[64], op=(lambda x: x * 7), test=(lambda x: 1 if x % 13 == 0 else 3)),
    Monkey(starting_items=[60, 84, 84, 65], op=(lambda x: x + 7), test=(lambda x: 2 if x % 19 == 0 else 7)),
    Monkey(starting_items=[52, 67, 74, 88, 51, 61], op=(lambda x: x * 3), test=(lambda x: 5 if x % 5 == 0 else 7)),
    Monkey(starting_items=[67, 72], op=(lambda x: x + 3), test=(lambda x: 1 if x % 2 == 0 else 2)),
    Monkey(starting_items=[80, 79, 58, 77, 68, 74, 98, 64], op=(lambda x: x * x), test=(lambda x: 6 if x % 17 == 0 else 0)),
    Monkey(starting_items=[62, 53, 61, 89, 86], op=(lambda x: x + 8), test=(lambda x: 4 if x % 11 == 0 else 6)),
    Monkey(starting_items=[86, 89, 82], op=(lambda x: x + 2), test=(lambda x: 3 if x % 7 == 0 else 0)),
    Monkey(starting_items=[92, 81, 70, 96, 69, 84, 83], op=(lambda x: x + 4), test=(lambda x: 4 if x % 3 == 0 else 5))
]

for monkey in monkeys:
    monkey.set_all_monkeys(monkeys)

for i in range(10000):
    for monkey in monkeys:
        monkey.act()

for monkey in monkeys:
    print(monkey.items, monkey.total_expected)

result = sorted([monkey.total_expected for monkey in monkeys], reverse=True)[0:2]
print(result[0] * result[1])