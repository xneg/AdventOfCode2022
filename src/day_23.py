from itertools import groupby


class Elf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.number = None
        self.x_proposed = x
        self.y_proposed = y
        self.strategies = [self.strategy_north, self.strategy_south, self.strategy_west, self.strategy_east]
        self.active = True

    def propose(self, elves):
        self.x_proposed = self.x
        self.y_proposed = self.y
        self.active = self.need_act(elves)
        if self.active:
            for strategy in self.strategies:
                result, (self.x_proposed, self.y_proposed) = strategy(elves)
                if result:
                    break
        self.strategies = self.strategies[1:] + [self.strategies[0]]
        return self.x_proposed, self.y_proposed

    def move(self, proposals):
        if (self.x_proposed, self.y_proposed) in proposals:
            self.x, self.y = self.x_proposed, self.y_proposed

    def need_act(self, elves):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (self.x + j, self.y + i) in elves:
                    return True
        return False

    def strategy_north(self, elves):
        next_y = self.y - 1
        for i in range(-1, 2):
            if (self.x + i, next_y) in elves:
                return False, (self.x, self.y)
        return True, (self.x, next_y)

    def strategy_south(self, elves):
        next_y = self.y + 1
        for i in range(-1, 2):
            if (self.x + i, next_y) in elves:
                return False, (self.x, self.y)
        return True, (self.x, next_y)

    def strategy_west(self, elves):
        next_x = self.x - 1
        for i in range(-1, 2):
            if (next_x, self.y + i) in elves:
                return False, (self.x, self.y)
        return True, (next_x, self.y)

    def strategy_east(self, elves):
        next_x = self.x + 1
        for i in range(-1, 2):
            if (next_x, self.y + i) in elves:
                return False, (self.x, self.y)
        return True, (next_x, self.y)

def draw(elves):
    # min_y = min(elf.y for elf in elves)
    # max_y = max(elf.y for elf in elves)
    # min_x = min(elf.x for elf in elves)
    # max_x = max(elf.x for elf in elves)

    min_y, max_y = -2, 9
    min_x, max_x = -3, 10

    # min_y, max_y = -1, 4
    # min_x, max_x = 0, 4
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # elf = [elf for elf in elves if elf.x == x and elf.y == y]
            if any(elf.x == x and elf.y == y for elf in elves):
                print('#', end='')
            # if len(elf) > 0:
            #     print(elf[0].number, end=' ')
            else:
                print('.', end='')
        print('')
    print('')

lines = open("../inputs/day_23.txt", "r").read().splitlines()

elves = [Elf(x, y) for y, line in enumerate(lines) for x, pos in enumerate(line) if pos == '#']
for idx, elf in enumerate(elves):
    elf.number = idx + 1

def process_elves():
    elves_coordinates = set([(elf.x, elf.y) for elf in elves])
    proposals = []
    for elf in elves:
        proposals.append(elf.propose(elves_coordinates))
    if not any(elf.active for elf in elves):
        return True
    uniq_proposals = set([key for key, group in groupby(sorted(proposals)) if len(list(group)) == 1])
    for elf in elves:
        elf.move(uniq_proposals)
    return False

# draw(elves)

# Part I
for i in range(10):
    process_elves()
    # draw(elves)
min_y = min(elf.y for elf in elves)
max_y = max(elf.y for elf in elves)
min_x = min(elf.x for elf in elves)
max_x = max(elf.x for elf in elves)

print((max_y - min_y + 1) * (max_x - min_x + 1) - len(elves))

# Part II
elves = [Elf(x, y) for y, line in enumerate(lines) for x, pos in enumerate(line) if pos == '#']

count = 0
while True:
    count = count + 1
    if process_elves():
        break
print(count)

