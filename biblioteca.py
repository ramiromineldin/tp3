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
        lista.append(heapq.heappop(heap)[1])
    return lista[::-1]
     
     
def page_rank(grafo, d, k):
    len_grafo = len(grafo) 
    pageranks_actuales = {}
    pageranks_anteriores = {}
    for vertice in grafo.vertices:
        pageranks_actuales[vertice] = 1/len_grafo
       
        
    for i in range(k):
        pageranks_anteriores = pageranks_actuales.copy() 
        for vertice in grafo.vertices:
            pagerank_sum = 0
            for ady in grafo.adyacentes(vertice):
                pagerank_sum +=pageranks_anteriores[ady] / len(grafo.adyacentes(ady))
            pageranks_actuales[vertice] = (1-d) / len_grafo + d * pagerank_sum

    return diccionario_a_lista_ordenada(pageranks_actuales)



def random_walk(grafo, vertice, k, pageranks,i):
    if i == k:
        return
    else:
        adyacentes = grafo.adyacentes(vertice)
        ady = random.choice(adyacentes)
        transferencia = pageranks[vertice] / len(adyacentes)
        pageranks[vertice] -= transferencia
        pageranks[ady] = pageranks.get(ady, 0) + transferencia        
        i+=1
        random_walk(grafo, ady, k, pageranks,i)


def page_rank_personalizado(grafo, vertice, k, n):
    pageranks = {}
    pageranks[vertice] = 1
    for i in range(n):
        random_walk(grafo, vertice, k, pageranks, 0)
    return diccionario_a_lista_ordenada(pageranks)


def clustering(grafo, vertice): 
	aristas_entre_adyacentes = 0
	adyacentes = len(grafo.adyacentes(vertice))
	clustering = 0
	if (adyacentes < 2): 
		return clustering

	for w in grafo.adyacentes(vertice): 
		for v in grafo.adyacentes(vertice): 
			if grafo.estan_unidos(grafo, v, w):
				aristas_entre_adyacentes += 1
		break

	clustering = (2 * aristas_entre_adyacentes) / (adyacentes * (adyacentes - 1))
	return clustering

def clustering_promedio(grafo): 
	suma = 0
	for v in grafo.obtener_vertices(): 
		suma +=  clustering(v)

	return suma/len(grafo)


g = Grafo(False)
g.agregar_vertice(1)
g.agregar_vertice(2)
g.agregar_vertice(3)
g.agregar_vertice(4)
g.agregar_vertice(5)
g.agregar_arista(1,2,None)
g.agregar_arista(1,3,None)
g.agregar_arista(2,3,None)
g.agregar_arista(2,4,None)
g.agregar_arista(3,5,None)
g.agregar_arista(4,5,None)
print(page_rank_personalizado(g, 1, 5, 10))






