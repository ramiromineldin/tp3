from collections import deque
from grafo import Grafo


def camino_mas_corto(grafo, origen, final):
    padres = bfs(grafo, origen, final)
    recorrido = []
    while final is not None:
        recorrido.append(final)
        final = padres[final]
    return recorrido[::-1]


def bfs(grafo, origen, final):
    visitados = set()
    padres = {}
    cola = deque()
    cola.append(origen)
    visitados.add(origen)
    padres[origen] = None
    while cola:
        v = cola.pop()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                cola.append(w)
                padres[w] = v
                if w == final:
                    return padres
    return -1



def page_rank(grafo, d):
    len_grafo = len(grafo)
    pageranks = {}
    for vertice in grafo.vertices:
        pageranks[vertice] = 1
    for vertice in grafo.vertices:
        pagerank_sum = sum(pageranks[ady] / len(grafo.adyacentes(ady)) for ady in grafo.adyacentes(vertice))
        pageranks[vertice] = (d / len_grafo + (1-d) * pagerank_sum)
    return pageranks



g = Grafo(False)
g.agregar_vertice(1)
g.agregar_vertice(2)
g.agregar_vertice(3)
g.agregar_vertice(4)
g.agregar_arista(1,2,None)
g.agregar_arista(2,3,None)
g.agregar_arista(3,4,None)
print(len(g))
print(page_rank(g, 0.85))





