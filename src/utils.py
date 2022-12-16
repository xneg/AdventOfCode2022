def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

class PriorityQueue:
    def __init__(self, queue):
        self.queue = queue

    def add(self, element):
        self.queue = sorted(self.queue + [element], key=lambda x: x[1], reverse=True)

    def pop(self):
        value, priority = self.queue.pop()
        return value