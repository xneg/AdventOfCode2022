def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0