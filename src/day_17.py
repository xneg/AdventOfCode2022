shapes = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
)
directions = {"<": (-1, 0), ">": (1, 0), "down": (0, -1)}
class Figure:
    def __init__(self, shape_idx, chamber, current_top):
        self.shape = [(point[0] + 2, point[1] + current_top + 3) for point in shapes[shape_idx]]
        self.chamber = chamber

    def move(self, direction):
        movement = directions[direction]
        next_position = [(point[0] + movement[0], point[1]) for point in self.shape]
        if self._check_available(next_position):
            return True, next_position
        else:
            return False, self.shape

    def _check_available(self, position):
        position_set = set(position)
        min_x = min([point[0] for point in position_set])
        max_x = max([point[0] for point in position_set])
        if min_x < 0 or max_x > 6:
            return False

        return len(set.intersection(position_set, self.chamber)) == 0

# lines = open("../inputs/day_16.txt", "r").read().splitlines()
input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
