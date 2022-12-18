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
        next_position = [(point[0] + movement[0], point[1] + movement[1]) for point in self.shape]
        if self._check_available(next_position):
            return True, next_position
        else:
            return False, self.shape

    def _check_available(self, position):
        position_set = set(position)
        min_x = min([point[0] for point in position_set])
        max_x = max([point[0] for point in position_set])
        min_y = min([point[1] for point in position_set])
        if min_x < 0 or max_x > 6 or min_y < 0:
            return False

        return len(set.intersection(position_set, self.chamber)) == 0

def calculate_height(input, limit, find_period=False):
    shape_index = 0
    chamber = set()
    current_figure = None
    command_index = 0
    figures_count = 0
    shape_command_set = {}
    while figures_count < limit:

        if current_figure is None:
            current_top = max(point[1] for point in chamber) + 1 if len(chamber) > 0 else 0
            current_figure = Figure(shape_index, chamber, current_top)
            shape_index = (shape_index + 1) % len(shapes)
            top_xs = [point[0] for point in chamber if point[1] == current_top - 1]
            if shape_index == 0 and (2 in top_xs or 3 in top_xs or 4 in top_xs) and find_period:
                if (shape_index, command_index) not in shape_command_set:
                    shape_command_set[(shape_index, command_index)] = figures_count, current_top
                else:
                    initial, initial_top = shape_command_set[(shape_index, command_index)]

                    return initial, initial_top, figures_count - initial, current_top - initial_top
        success, new_shape = current_figure.move(input[command_index])
        if success:
            current_figure.shape = new_shape
        success, new_shape = current_figure.move("down")
        if success:
            current_figure.shape = new_shape
        else:
            chamber.update(set(new_shape))
            current_figure = None
            figures_count = figures_count + 1
            if figures_count % 10 == 0:
                y_max = max(point[1] for point in chamber)
                chamber = set([point for point in chamber if point[1] + 50 > y_max])

        command_index = (command_index + 1) % len(input)
    return max(point[1] for point in chamber) + 1, chamber

lines = open("../inputs/day_17.txt", "r").read().splitlines()
input = lines[0]
# input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

# Part I
print("Part I", calculate_height(input, limit=2022)[0])

# Part II
initial, initial_top, period, addition = calculate_height(input, limit=4000, find_period=True)
max_to_check = 1000000000000
periods_count = (max_to_check - initial) // period
odd = max_to_check - initial - period * periods_count
print("Part II", calculate_height(input, limit=odd+initial)[0] + addition * periods_count)
