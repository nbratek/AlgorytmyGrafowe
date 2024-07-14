import dimacs
from queue import PriorityQueue

filename = "mc1"

V, L = dimacs.loadWeightedGraph(filename)
solution = dimacs.readSolution(filename)

adjlist = [{} for i in range(V + 1)]

for (u, v, c) in L:
    adjlist[u][v] = c
    adjlist[v][u] = c


def mergeVertices(G, x, y):
    for v in G[y]:
        if v != x:
            if v in G[x]:
                G[x][v] += G[y][v]
            else:
                G[x][v] = G[y][v]
    G[y] = {}
    for v in range(len(G)):
        if y in G[v]:
            if v != x:
                if x in G[v]:
                    G[v][x] += G[v][y]
                else:
                    G[v][x] = G[v][y]
            del G[v][y]


def minimumCutPhase(G):
    a = 1
    L = [a]
    S = set([a])
    suma_wag_krawedzi = {}

    PQ = PriorityQueue()

    for i in range(len(G)):
        if i != a and G[i] != {}:
            suma_wag_krawedzi[i] = -G[i].get(a, 0)
            PQ.put((suma_wag_krawedzi[i], i))

    while not PQ.empty():
        _, v = PQ.get()
        if v not in S:
            L.append(v)
            S.add(v)
            for u in G[v]:
                if u not in S:
                    suma_wag_krawedzi[u] -= G[v][u]
                    PQ.put((suma_wag_krawedzi[u], u))

    s = L[-1]
    t = L[-2]

    potencjalny_wynik = -suma_wag_krawedzi[s]

    mergeVertices(G, s, t)

    return potencjalny_wynik


def minimumCut(G):
    wynik = float("inf")
    for i in range(len(G) - 2):
        wynik = min(wynik, minimumCutPhase(G))
    return wynik


print("rozwiązanie: ", minimumCut(adjlist))
print("Rozwiązanie z pliku: ", solution)