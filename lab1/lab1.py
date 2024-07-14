import dimacs

s = 1
t = 2

filename = "graphs-lab1/clique20"

V, L = dimacs.loadWeightedGraph(filename)
solution = dimacs.readSolution(filename)

adjlist = [[] for i in range(V + 1)]

minc = -1
maxc = -1

for (u, v, c) in L:
    if c < minc or minc == -1:
        minc = c
    if c > maxc or maxc == -1:
        maxc = c
    adjlist[u].append((v,c))
    adjlist[v].append((u,c))

def dfs(adjlist, s, t, minw):
    def dfs_visit(u):
        visited[u] = True
        for (v, c) in adjlist[u]:
            if not visited[v] and c >= minw:
                dfs_visit(v)
    visited = [ False for i in range(len(adjlist))]
    dfs_visit(s)
    return visited[t]

def dfs_bin(val):
    return dfs(adjlist, s, t, val)

def binary_search(l, r, fn):
    while l <= r:
        mid = (l + r) // 2
        if fn(mid):
            l = mid + 1
        else:
            r = mid - 1
    return r

print("moj wynik", binary_search(minc, maxc, dfs_bin))
print("solution", solution)