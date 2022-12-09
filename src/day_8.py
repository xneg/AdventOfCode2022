lines = open("../inputs/day_8.txt", "r").read().splitlines()

matrix = [[int(c) for c in [*line]] for line in lines]
pivoted_matrix = [[row[i] for row in matrix] for i in range(len(matrix))]

def get_visible_trees(matrix):
    result = set()
    for y, row in enumerate(matrix):
        max_height = -1
        for x, cell in enumerate(row):
            if cell > max_height:
                result.add((x, y))
                max_height = cell
        max_height = -1
        for x, cell in enumerate(reversed(row)):
            if cell > max_height:
                result.add((len(row) - x - 1, y))
                max_height = cell
    return result

def calculate_score(x: int, y: int, matrix, pivoted_matrix):
    height = matrix[y][x]

    right = get_line_of_sight(height, matrix[y][x + 1:])
    left = get_line_of_sight(height, reversed(matrix[y][0:x]))
    bottom = get_line_of_sight(height, pivoted_matrix[x][y + 1:])
    up = get_line_of_sight(height, reversed(pivoted_matrix[x][0:y]))

    return right * left * bottom * up

def get_line_of_sight(height, row):
    total = 0
    for idx, cell in enumerate(row):
        total = total + 1
        if cell >= height:
            break
    return total

left_right_visible = get_visible_trees(matrix)
top_down_visible = get_visible_trees(pivoted_matrix)
seen_trees = left_right_visible | { (cell[1], cell[0]) for cell in top_down_visible}
print(len(seen_trees))

print(max([calculate_score(x=x, y=y, matrix=matrix, pivoted_matrix=pivoted_matrix)
           for y in range(len(matrix)) for x in range(len(matrix[0]))]))
