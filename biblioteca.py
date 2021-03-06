from collections import deque
import heapq
from grafo import Grafo
import random


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




def diccionario_a_lista_ordenada(diccionario):
    heap = []
    lista = []
    for item in list(diccionario.items()):
        heapq.heappush(heap,item[::-1])
    
    for i in range(len(heap)):
        lista.append(heapq.heappop(heap))
    return lista[::-1]
    
    
def page_rank(grafo, d, n):
    len_grafo = len(grafo)
    pageranks = {}
    i = 0
    for vertice in grafo.vertices:
            pageranks[vertice] = 1.0/len_grafo
    while (i < n):    
        for vertice in grafo.vertices:
            pagerank_sum = sum(pageranks[ady] / len(grafo.adyacentes(ady)) for ady in grafo.adyacentes(vertice))
            pageranks[vertice] += ((1-d) / len_grafo + (d * pagerank_sum))
        i+=1
    
    return diccionario_a_lista_ordenada(pageranks)
     




def random_walk(grafo, vertice, pagerank, n, largo):
    for vertice in grafo.vertices:
        for i in range(n):
            for j in range(largo):
                adyacentes = grafo.adyacentes(vertice)
                random.choice(adyacentes)
                



def page_rank_personalizado(grafo, vertice, n):
    pagerank = {}
    for vertice in grafo.vertices:
        pagerank[vertice] = 1
    for v in grafo.adyacentes(vertice):
        pagerank[v] *= 1/len(grafo.adyacentes(v))




g = Grafo(False)
g.agregar_vertice(1)
g.agregar_vertice(2)
g.agregar_vertice(3)
g.agregar_vertice(4)
g.agregar_vertice(5)
g.agregar_arista(1,2,None)
g.agregar_arista(2,3,None)
g.agregar_arista(3,4,None)
g.agregar_arista(3,5,None)
print(len(g))
print(page_rank(g, 0.8, 5))







