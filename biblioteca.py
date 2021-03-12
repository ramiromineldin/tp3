from collections import deque
import heapq
from grafo import Grafo
import random
import csv
import sys
sys.setrecursionlimit(50000)
csv.field_size_limit(sys.maxsize)



def grafo_crear_estructura(ruta_archivo):
    """Recibe una ruta de archivo, lee el contenido y devuelve un grafo no dirigido donde las canciones y los usuarios son los vertices, 
    las aristas conecta usuarios con vertices si el usuario tiene una playlist con esta cancion y el peso de la arista el nombre la playlist, 
    un diccionario donde las claves son las playlist y los datos son una lista de canciones que pertencen a la playlist 
    y por ultimo devuelve un set que tiene los nombres de todos los usuarios"""
    
    canciones_usuarios = Grafo(False)
    canciones_por_playlist = {}
    usuarios = set()
    with open(ruta_archivo) as archivo:
        reader = csv.reader(archivo, delimiter = "\t")
        next(reader)
        for row in reader:
            if len(row) != 7: continue
            id_n, user_id, track_name, artist, playlist_id, playlist_name, genres = row
            cancion = "{} - {}".format(track_name,artist)
            canciones_usuarios.agregar_vertice(user_id)
            canciones_usuarios.agregar_vertice(cancion)
            canciones_usuarios.agregar_arista(user_id,cancion, playlist_name)

            canciones_por_playlist[playlist_name] = canciones_por_playlist.get(playlist_name, [])
            if cancion not in canciones_por_playlist[playlist_name]:
                canciones_por_playlist[playlist_name].append(cancion)
            
            usuarios.add(user_id)

    return canciones_por_playlist, canciones_usuarios, usuarios

def grafo_crear_estructura_2(canciones_por_playlist):
    """Recibe un diccionario donde las claves son las playlist y los datos son una lista de canciones que pertencen a la playlist 
    y devuelve un grafo no pesado donde los vertices son las canciones y las aristas relacionan a las canciones que pertenecen a una 
    misma playlist."""
    
    red_canciones = Grafo(False)
    for playlist in canciones_por_playlist:
        for i in canciones_por_playlist[playlist]:
            red_canciones.agregar_vertice(i)
            for j in canciones_por_playlist[playlist]:
                if i != j:
                    red_canciones.agregar_vertice(j)
                    red_canciones.agregar_arista(i , j, None)

    return red_canciones



def camino_mas_corto(grafo, origen, final):
    """Recibe un grafo, un vertice de origen y un vertice final, halla el camino mas corto entre el origen y el final y 
    devuelve una lista con el camino. En caso de no haber un camino devuelve None"""

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
        if v == final: return padres
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                cola.append(w)
                padres[w] = v
    return None




def diccionario_a_lista_ordenada(diccionario):
    """Recibe un diccionario, ordena los datos del diccionario de menor a mayor, una lista con sus respectivas claves ordenadas de 
    mayor a menor por el criterio anterior"""
    heap = []
    lista = []
    for item in list(diccionario.items()):
        heapq.heappush(heap,item[::-1])

    for i in range(len(heap)):
        lista.append(heapq.heappop(heap)[1])
    return lista[::-1]
     
     
def page_rank(grafo, d, k):
    """ Itera k veces el grafo y calcula el page rank de cada vertice. Devuelve una lista con los vertices ordenados de mayor a 
    menor dependiendo de su page rank."""
    
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


def wrp_page_rank_personalizado(grafo, vertice, k, pageranks,j):
    if j == k:
        return
    else:
        adyacentes = grafo.adyacentes(vertice)
        ady = random.choice(adyacentes)
        transferencia = pageranks[vertice] / len(adyacentes)
        pageranks[vertice] -= transferencia
        pageranks[ady] = pageranks.get(ady, 0) + transferencia        
        wrp_page_rank_personalizado(grafo, ady, k, pageranks, j + 1)


def page_rank_personalizado(grafo, canciones, k, n):
    """
    Calcula el PageRank Personalizado de los vertices del grafo empezando desde el vertice pasado por parametro y devuelve una lista 
    de los vertices ordenada de mayor a menor segun PageRank. 
    grafo: grafo fue creado
    vertice: vertice del grafo
    k: longitud de camino de RandomWalks 
    n: cantidad de iteraciones para el PageRank 
    """

    pageranks = {}
    for cancion in canciones: 
        pageranks[cancion] = 1
    for cancion in canciones: 
        for i in range(n):
            wrp_page_rank_personalizado(grafo, cancion, k, pageranks, 0)
    return diccionario_a_lista_ordenada(pageranks)


   
def wrp_obtener_ciclo(grafo, inicio, v, visitados, camino, n): 
    camino.append(v)
    visitados.add(v)
    if len(camino) == n and inicio in grafo.adyacentes(v) and len(camino) > 2:
        camino.append(inicio)
        return True
    for w in grafo.adyacentes(v): 
        if len(camino) >= n: break
        if w not in visitados: 
            if wrp_obtener_ciclo(grafo, inicio, w, visitados, camino, n):  
                return True

    if len(visitados) != 0 and v in visitados:
        visitados.remove(v)
    camino.pop()
    return False


def obtener_ciclo(grafo, inicio, n):
    """
    Calcula un ciclo de largo n desde desde y hasta un vertice n. Devuelve la lista con los vertices de dicho ciclo, en caso
    de no encontrarse devuelve None. 
    grafo: grafo fue creado
    inicio: vertice del grafo
    n: longitud del ciclo
    """

    camino = []
    visitados = set()
    if wrp_obtener_ciclo(grafo, inicio, inicio, visitados, camino, n):
            return camino
    return None


def calcular_clustering(grafo, vertice): 
    """
    Calcula el clustering de un vertice del grafo y devuelve su valor  
    grafo: grafo fue creado 
    vertice: vertice del grafo
    """
    
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
    """
    Calcula el clustering promedio del grafo entero y devuelve su valor
    grafo: grafo fue creado 
    """

    suma = 0
    for v in grafo.obtener_vertices(): 
        suma +=  calcular_clustering(grafo, v)

    return suma/len(grafo)

def rango_n(grafo, origen, n):
    """ 
    Calcula la cantidad de vertices que se encuentran a una distancia n del vertice pasado por parametro, y devuelve la cantidad
    grafo: grafo fue creado
    origen: vertice del grafo
    n: distancia entre vertices 
    """

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

