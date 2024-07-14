import dimacs
import copy

filename = "vcover/interval-rnd100"

V, L = dimacs.loadWeightedGraph(filename)
solution = dimacs.readSolution(filename)

setlist = [set() for i in range(V + 1)]

for (u, v, c) in L:
    setlist[u].add(v)
    setlist[v].add(u)


def lexBFS(setlist):
    V = len(setlist) - 1
    lista = [[i for i in range(V, 0, -1)]]

    kolejnosc = []
    while len(lista) > 0:
        ostatni_element = lista[-1]
        print("Lista:", lista)
        wierzchołek = ostatni_element.pop()
        print("Wierzchołek:", wierzchołek)
        kolejnosc.append(wierzchołek)

        nowa_lista = []
        for X in lista:
            Y = []  # Wierzchołki połączone z wierzchołkiem w grafie
            K = []  # Wierzchołki niepołączone z wierzchołkiem w grafie
            for v in X:
                if v in setlist[wierzchołek]:
                    Y.append(v)
                else:
                    K.append(v)
            if len(K) > 0:
                nowa_lista.append(K)
            if len(Y) > 0:
                nowa_lista.append(Y)
        lista = copy.deepcopy(nowa_lista)
    return kolejnosc


def is_perfect_elimination_ordering(kolejnosc, setlist):
    V = len(kolejnosc)
    RN = [set() for i in range(V + 1)]
    parent = [-1 for i in range(V + 1)]

    odwiedzone = set()

    for v in kolejnosc:
        RN[v] = odwiedzone & setlist[v]
        for u in setlist[v]:
            if u not in odwiedzone:
                parent[u] = v
        odwiedzone.add(v)
    for v in kolejnosc:
        if not (RN[v] - {parent[v]} <= RN[parent[v]]):
            return False
    return True


def maxClique(kolejnosc, setlist):
    V = len(kolejnosc)
    RN = [set() for i in range(V + 1)]

    odwiedzone = set()

    for v in kolejnosc:
        RN[v] = odwiedzone & setlist[v]
        odwiedzone.add(v)

    odpowiedz = 0
    for v in kolejnosc:
        klika = len(RN[v]) + 1
        if klika > odpowiedz:
            odpowiedz = klika
    return odpowiedz


def minColoring(kolejnosc, setlist):
    V = len(kolejnosc)
    color = [0 for i in range(V + 1)]

    for v in kolejnosc:
        adjcolor = set()
        for u in setlist[v]:
            adjcolor.add(color[u])
        color[v] = 1
        while color[v] in adjcolor:
            color[v] += 1
    return max(color)


def vertexCover(kolejnosc, setlist):
    V = len(kolejnosc)
    odwrotna_kolejnosc = kolejnosc[::-1]

    pokrycie = set()

    for v in odwrotna_kolejnosc:
        if setlist[v] & pokrycie == set():
            pokrycie.add(v)

    return V - len(pokrycie)


# Tylko do testowania - można usunąć
class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()  # zbiór sąsiadów

    def connect_to(self, v):
        self.out.add(v)


G = [None] + [Node(i) for i in range(1, V + 1)]  # żeby móc indeksować numerem wierzchołka

for (u, v, _) in L:
    G[u].connect_to(v)
    G[v].connect_to(u)


def checkLexBFS(vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            Ni = G[vs[i]].out
            Nj = G[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True




order = lexBFS(setlist)

print("Test:", checkLexBFS(order))
# print("Czy jest PDO:", is_perfect_elimination_ordering(order, setlist))
# print("Maksymalna klika:", maxClique(order, setlist))
# print("Minimalne kolorowanie:", minColoring(order, setlist))
print("Pokrycie wierzchołkowe:", vertexCover(order, setlist))
print("Poprawna odpowiedz:", solution)
