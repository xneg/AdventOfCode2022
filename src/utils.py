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


# utility function to form edge between two vertices
# source and dest
def add_edge(adj, src, dest):
    adj[src].append(dest);
    adj[dest].append(src);


# a modified version of BFS that stores predecessor
# of each vertex in array p
# and its distance from source in array d
def BFS(adj, src, dest, v, pred, dist):
    # a queue to maintain queue of vertices whose
    # adjacency list is to be scanned as per normal
    # DFS algorithm
    queue = []

    # boolean array visited[] which stores the
    # information whether ith vertex is reached
    # at least once in the Breadth first search
    visited = [False for i in range(v)];

    # initially all vertices are unvisited
    # so v[i] for all i is false
    # and as no path is yet constructed
    # dist[i] for all i set to infinity
    for i in range(v):
        dist[i] = 1000000
        pred[i] = -1;

    # now source is first to be visited and
    # distance from source to itself should be 0
    visited[src] = True;
    dist[src] = 0;
    queue.append(src);

    # standard BFS algorithm
    while (len(queue) != 0):
        u = queue[0];
        queue.pop(0);
        for i in range(len(adj[u])):

            if (visited[adj[u][i]] == False):
                visited[adj[u][i]] = True;
                dist[adj[u][i]] = dist[u] + 1;
                pred[adj[u][i]] = u;
                queue.append(adj[u][i]);

                # We stop BFS when we find
                # destination.
                if (adj[u][i] == dest):
                    return True;

    return False;


# utility function to print the shortest distance
# between source vertex and destination vertex
def printShortestDistance(adj, s, dest, v):
    # predecessor[i] array stores predecessor of
    # i and distance array stores distance of i
    # from s
    pred = [0 for i in range(v)]
    dist = [0 for i in range(v)];

    if (BFS(adj, s, dest, v, pred, dist) == False):
        pass
        # print("Given source and destination are not connected")

    # vector path stores the shortest path
    path = []
    crawl = dest;
    path.append(crawl);

    while (pred[crawl] != -1):
        path.append(pred[crawl]);
        crawl = pred[crawl];

    return dist[dest], [path[i] for i in range(len(path) - 1, -1, -1)]