def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

class Particle:
    directions = {
        "L": (-1, 0),
        "R": (1, 0),
        "D": (0, -1),
        "U": (0, 1)
    }
    def __init__(self):
        self.x = 0
        self.y = 0

    def direction(self, other: "Particle"):
        x_dir = sign(other.x - self.x) if abs(other.x - self.x) > 1 \
                                          or (abs(other.x - self.x) > 0 and abs(other.y - self.y) > 1) else 0
        y_dir = sign(other.y - self.y) if abs(other.y - self.y) > 1 \
                                          or (abs(other.x - self.x) > 1 and abs(other.y - self.y) > 0) else 0
        return x_dir, y_dir

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

def calculate_movement(particles, input):
    path = []
    for line in input:
        direction, distance = line.split(' ')
        for i in range(int(distance)):
            particles[0].move(*Particle.directions[direction])
            for idx, p in enumerate(particles[1:]):
                direction = p.direction(particles[idx])
                p.move(*direction)
            path.append((particles[-1].x, particles[-1].y))
    return path

lines = open("../inputs/day_9.txt", "r").read().splitlines()

print(len(set(calculate_movement([Particle() for _ in range(2)], lines))))
print(len(set(calculate_movement([Particle() for _ in range(10)], lines))))
