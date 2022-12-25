def from_snafu(snafu_str):
    snafu_map = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
    return sum([snafu_map[v] * pow(5, idx) for idx, v in enumerate(reversed(snafu_str))])

def to_snafu(value):
    snafu_map = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    result = []
    current = value
    skip_nulls = 0
    while current > 0:
        next, remainder = divmod(current, 5)
        if remainder == 0 and skip_nulls > 0:
            current = next
            skip_nulls = skip_nulls - 1
            continue
        if remainder <= 2:
            result.append(remainder)
            current = next
        else:
            result.append(remainder - 5)
            current = current + (5 - remainder)
            skip_nulls = skip_nulls + 1
    return list(reversed([snafu_map[r] for r in result]))

lines = open("../inputs/day_25.txt", "r").read().splitlines()

decimal_result = sum([from_snafu(line) for line in lines])
print(decimal_result)
print(*to_snafu(decimal_result), sep='')
