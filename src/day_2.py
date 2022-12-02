symbol_costs = {"A": 1, "B": 2, "C": 3}
outcome_matrix = {
    ("A", "A"): 3,
    ("A", "B"): 6,
    ("A", "C"): 0,
    ("B", "A"): 0,
    ("B", "B"): 3,
    ("B", "C"): 6,
    ("C", "A"): 6,
    ("C", "B"): 0,
    ("C", "C"): 3,
}

elf_symbols = ["A", "B", "C"]  # Rock Paper Scissors A < B < C < A
my_symbols = [
    "X",
    "Y",
    "Z",
]  # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.


def get_symbol_1(elf_symbol, my_symbol):
    return elf_symbols[my_symbols.index(my_symbol)]


def get_symbol_2(elf_symbol, my_symbol):
    idx = elf_symbols.index(elf_symbol)
    outcome = my_symbols.index(my_symbol) - 1
    return elf_symbols[(idx + outcome) % 3]


def calculate_outcome(elf_symbol, my_symbol):
    return symbol_costs[my_symbol] + outcome_matrix[(elf_symbol, my_symbol)]


def get_result(pairs, get_symbol_func):
    results = list(map(lambda x: calculate_outcome(x[0], get_symbol_func(*x)), pairs))
    return sum(results)


lines = open("../inputs/day_2.txt", "r").read().splitlines()

pairs = []
for line in lines:
    pairs.append(tuple(line.split(" ")))

print(get_result(pairs, get_symbol_1))
print(get_result(pairs, get_symbol_2))
