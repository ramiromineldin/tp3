from collections import deque
import heapq
from grafo import Grafo
import random
import csv


def grafo_crear_estructura_1(ruta_archivo):
    canciones_usuarios = Grafo(False)
    canciones_por_playlist = {}
    usuarios = set()
    with open(ruta_archivo) as archivo:
        reader = csv.reader(archivo, delimiter = "\t")
        for row in reader:
            id, user_id, track_name, artist, playlist_id, playlist_name, genres = row
            canciones_usuarios.agregar_vertice(user_id)
            canciones_usuarios.agregar_vertice("{}-{}".format(track_name,artist))
            canciones_usuarios.agregar_arista(user_id,"{}-{}".format(track_name,artist), playlist_name)

            canciones_por_playlist[playlist_name] = canciones_por_playlist.get(playlist_name, []).append("{}-{}".format(track_name,artist))
            
            usuarios.add(user_id)

    return canciones_por_playlist, canciones_usuarios, usuarios

def grafo_crear_estructura_2(canciones_por_playlist):
    canciones = Grafo(False)
    for playlist in canciones_por_playlist:
        for i in canciones_por_playlist[playlist]:
            canciones.agregar_vertice(i)
            for j in canciones_por_playlist[playlist]:
                if i != j:
                    canciones.agregar_vertice(j)
                    canciones.agregar_arista(i , j, playlist)
    return canciones



def camino_mas_corto(grafo, origen, final):
    padres = bfs_camino_corto(grafo, origen, final)
    recorrido = []
    if padres != None:
        while final is not None:
            recorrido.append(final)
            aux = final
            final = padres[final]
            peso = grafo.peso_arista(aux, final)
            if peso:
                recorrido.append(peso)
        return recorrido[::-1]
    return padres


def bfs_camino_corto(grafo, origen, final):
    visitados = set()
    padres = {}
    cola = deque()                
    cola.append(origen)
    visitados.add(origen)
    padres[origen] = None
    while cola:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                cola.append(w)
                padres[w] = v
                if w == final:
                    return padres
    return None




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



def wrp_obtener_ciclo(grafo, inicio, actual, visitados, n, i, padres): 
    if (i == n and inicio == actual): return padres
    if i > n: return None

    for w in grafo.adyacentes(actual):
        if (w in visitados and w != inicio) or padres[actual] == w: continue
        padres[w] = actual
        visitados.add(w)
        ciclo = wrp_obtener_ciclo(grafo, inicio, w, visitados, n, i + 1, padres)
        visitados.remove(w)
        if ciclo: return padres
        
    return None

def obtener_ciclo(grafo, inicio, n):
    visitados = set()
    visitados.add(inicio)
    padres = {}
    padres[inicio] = None
    return  wrp_obtener_ciclo(grafo, inicio, inicio, visitados, n,0, padres)


def calcular_clustering(grafo, vertice): 
    aristas_entre_adyacentes = 0
    adyacentes = len(grafo.adyacentes(vertice))
    clustering = 0
    if (adyacentes < 2): 
        return clustering

    for w in grafo.adyacentes(vertice): 
        for v in grafo.adyacentes(vertice): 
            if grafo.estan_unidos(v, w):
                aristas_entre_adyacentes += 1

    clustering = aristas_entre_adyacentes / (adyacentes * (adyacentes - 1))
    return clustering

def clustering_promedio(grafo): 
    suma = 0
    for v in grafo.obtener_vertices(): 
        suma +=  clustering(grafo, v)

    return suma/len(grafo)


def rango_n(grafo, origen, n):
    visitados = set()
    orden = {}
    orden[origen] = 0
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    cantidad_a_dist_n = 0    
    while cola:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                orden[w] = orden[v] + 1
                visitados.add(w)
                cola.append(w)
    
    for vertice in orden:
        if orden[vertice] == n:
            cantidad_a_dist_n += 1
    return cantidad_a_dist_n

