import dimacs
import copy

filename = "clique5"

V, L = dimacs.loadWeightedGraph(filename)
solution = dimacs.readSolution(filename)

adjmatrix = [[0 for i in range(V + 1)] for i in range(V + 1)]

for (u, v, c) in L:
    adjmatrix[u][v] += c
    adjmatrix[v][u] += c


def bfs(adjmatrix, s, t):
    i = 0
    queue = [s]
    V = len(adjmatrix)
    previous = [-1 for i in range(V)]
    previous[s] = 0

    while i < len(queue):
        u = queue[i]

        for v in range(V):
            if adjmatrix[u][v] > 0 and previous[v] == -1:
                previous[v] = u
                queue.append(v)

        i += 1

    # Zwracamy ścieżkę od s do t
    if previous[t] == -1:
        return []
    path = []
    u = t
    while u != 0:
        path.append(u)
        u = previous[u]
    path.reverse()

    return path


def fordfulkerson(adjmatrix, s, t, find_path):
    V = len(adjmatrix)
    flow = [[0 for i in range(V)] for i in range(V)]
    residual = copy.deepcopy(adjmatrix)

    path = find_path(residual, s, t)

    while len(path) > 0:
        minimum = residual[path[0]][path[1]]
        for i in range(len(path) - 1):
            minimum = min(minimum, residual[path[i]][path[i + 1]])
        for i in range(len(path) - 1):
            flow[path[i]][path[i + 1]] += minimum
            flow[path[i + 1]][path[i]] -= minimum
        for i in range(V):
            for j in range(V):
                residual[i][j] = adjmatrix[i][j] - flow[i][j]

        path = find_path(residual, s, t)

    sum_flow = 0
    for i in range(V):
        sum_flow += flow[s][i]
    return sum_flow


min_cut = float('inf')

for s in range(1, V + 1):
    for t in range(s + 1, V + 1):
        cut = fordfulkerson(adjmatrix.copy(), s, t, bfs)
        if cut < min_cut:
            min_cut = cut

print("odpowiedz:", min_cut)
print("Poprawna odpowiedz:", solution)