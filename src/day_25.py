def from_snafu(snafu_str):
    snafu_map = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
    return sum([snafu_map[v] * pow(5, idx) for idx, v in enumerate(reversed(snafu_str))])

def to_snafu(value):
    snafu_map = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    intermediate = []
    while value > 0:
        value, remainder = divmod(value, 5)
        intermediate.append(remainder)

    result = []
    acc = 0

    for i in intermediate:
        current = i + acc
        if current <= 2:
            result.append(current)
            acc = 0
        else:
            result.append(current - 5)
            acc = 1
    if acc != 0: result.append(acc)
    return list(reversed([snafu_map[r] for r in result]))


lines = open("../inputs/day_25.txt", "r").read().splitlines()

decimal_result = sum([from_snafu(line) for line in lines])
print(decimal_result)
print(*to_snafu(decimal_result), sep='')
