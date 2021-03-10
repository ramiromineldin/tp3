import biblioteca
import imprimir
import sys

def camino(canciones_usuarios, origen, final):
    recorrido = biblioteca.camino_mas_corto(canciones_usuarios, origen, final)
    if recorrido != None:
        imprimir.imprimir_camino(recorrido)
    else:
        print("No se encontro el recorrido")
    return

def mas_importantes(canciones_usuarios, usuarios, n):
    pageranks = biblioteca.page_rank(canciones_usuarios, 0.85, 20)
    canciones_mas_importantes = []
    tam_lista = 0
    for elemento in pageranks:
        if tam_lista == n:
            break
        if not elemento in usuarios:
            canciones_mas_importantes.append(elemento)
            tam_lista += 1
    imprimir.imprimir_puntocoma(canciones_mas_importantes)
    return
        
def recomendacion(canciones_usuarios, elemento, usuarios, n):
    pageranks = biblioteca.page_rank_personalizado(canciones_usuarios, elemento, 15, 1000)

    recomendacion = []
    tam_lista = 0
    es_usuario = False

    if elemento in usuarios:
        es_usuario = True
    
    for i in pageranks:
        if tam_lista == n:
            break
        if (es_usuario and i in usuarios) or (not es_usuario and i not in usuarios):
            recomendacion.append(i)
            tam_lista += 1
    imprimir.imprimir_puntocoma(recomendacion)
    return

    #REVISAR OBTENER CICLO EN BIBLIOTECA
def ciclo_n_canciones(canciones, n, cancion):
    ciclo = biblioteca.obtener_ciclo(canciones, cancion, n)
    imprimir.imprimir_flechas(ciclo)
    return


def rango(canciones, n, cancion):
    return biblioteca.rango_n(canciones, cancion, n)


def clustering(canciones, cancion):
    if cancion:
        return biblioteca.calcular_clustering(canciones, cancion)
    return biblioteca.clustering_promedio(canciones)


def procesar_entrada(canciones_usuarios, canciones_por_playlist):
    for row in sys.stdin:
        entrada = row.split()
        