import dimacs

filename = "flow/clique5"


V, L = dimacs.loadDirectedWeightedGraph(filename)
solution = dimacs.readSolution(filename)
s, t = 1, V

adjmatrix = [[0 for i in range(V + 1)] for i in range(V + 1)]

for (u, v, c) in L:
    adjmatrix[u][v] += c


def bfs(adjmatrix, s, t):
    i = 0
    queue = [s]
    V = len(adjmatrix)
    previous = [-1 for i in range(V)]
    previous[s] = 0

    while i < len(queue):
        u = queue[i]

        for v in range(V):
            if adjmatrix[u][v] > 0 and previous[v] == -1:  # previous[v] == -1 oznacza, że wierzchołek v nie był jeszcze odwiedzony
                previous[v] = u
                queue.append(v)
        i += 1

    # ścieżka od s do t
    if previous[t] == -1:
        return []
    path = []
    u = t
    while u != 0:
        path.append(u)
        u = previous[u]
    path.reverse()
    return path



def fordfulkerson(adjmatrix, s, t):
    V = len(adjmatrix)
    flow = [[0 for i in range(V)] for i in range(V)]
    path = bfs(adjmatrix, s, t)
    while len(path) > 0:
        minimum = adjmatrix[path[0]][path[1]]
        for i in range(len(path) - 1):
            minimum = min(minimum, adjmatrix[path[i]][path[i + 1]])
        for i in range(len(path) - 1):
            flow[path[i]][path[i + 1]] += minimum
            flow[path[i + 1]][path[i]] -= minimum
        residual = adjmatrix.copy()
        for i in range(V):
            for j in range(V):
                residual[i][j] -= flow[i][j]
        path = bfs(residual, s, t)
    sum_flow = 0
    for i in range(V):
        sum_flow += flow[s][i]
    return sum_flow


print("Poprawna odpowiedz:", solution)
print("bfs:", fordfulkerson(adjmatrix, s, t))