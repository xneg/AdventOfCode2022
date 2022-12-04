class Range:
    @staticmethod
    def from_string(s: str) -> "Range":
        start, end = s.split("-")
        return Range(int(start), int(end))
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other: "Range"):
        return self.start <= other.start and self.end >= other.end

    def overlap(self, other: "Range"):
        return self.start <= other.end and self.end >= other.start

lines = open("../inputs/day_4.txt", "r").read().splitlines()

def range_pairs(lines):
     return [list(map(lambda x: Range.from_string(x), pair))
             for pair in
             list(map(lambda x: x.split(","), lines))]

pairs = range_pairs(lines)

print(len(list(filter(lambda p: p[0].contains(p[1]) or p[1].contains(p[0]), pairs))))
print(len(list(filter(lambda p: p[0].overlap(p[1]), pairs))))