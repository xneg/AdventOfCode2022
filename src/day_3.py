def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def first_part_sets(line):
    half = len(line) // 2
    return [set(line[:half]), set(line[half:])]

def second_part_sets(group):
    return list(map(set, group))

def total(inputs, set_calculator):
    def get_value(ch: str):
        if ch.lower() == ch:
            return ord(ch) - 96
        return ord(ch) - 38

    sets_list = map(set_calculator, inputs)
    return sum(map(lambda x: get_value(*set.intersection(*x)), sets_list))

lines = open("../inputs/day_3.txt", "r").read().splitlines()

print(total(lines, first_part_sets))
print(total(chunker(lines, 3), second_part_sets))
