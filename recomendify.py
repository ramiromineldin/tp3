#!/usr/bin/env python3
import biblioteca
import imprimir
import sys
import random


def camino(canciones_usuarios, origen, final, usuarios):
    if origen in usuarios or final in usuarios: 
        print("Tanto el origen como el destino deben ser canciones")

    else:
        recorrido = biblioteca.camino_mas_corto(canciones_usuarios, origen, final)

        if recorrido != None:
            imprimir.imprimir_camino(recorrido)

        else:
            print("No se encontro el recorrido")
    return

def mas_importantes(canciones_usuarios, usuarios, n, pagerank_ya_calculado):
    if len(pagerank_ya_calculado) == 0:
        pagerank_ya_calculado = biblioteca.page_rank(canciones_usuarios, 0.85, 20)

    canciones_mas_importantes = []
    tam_lista = 0
    for elemento in pagerank_ya_calculado:
        if tam_lista == n:
            break
        if not elemento in usuarios:
            canciones_mas_importantes.append(elemento)
            tam_lista += 1
    imprimir.imprimir_puntocoma(canciones_mas_importantes)
    return
        
def recomendacion(canciones_usuarios, elemento,tipo, usuarios, n,):
    pageranks = biblioteca.page_rank_personalizado(canciones_usuarios, elemento, 100, 15)
    print(len(pageranks))
    recomendacion = []
    es_usuario = False

    if tipo == "usuarios":
        es_usuario = True
    
    for i in pageranks:
        if len(recomendacion) == n:
            break

        if i == elemento: continue

        elif (es_usuario and i in usuarios) or (not es_usuario and i not in usuarios):
            recomendacion.append(i)

    imprimir.imprimir_puntocoma(recomendacion)

    
    return

def ciclo_n_canciones(red_canciones, n, cancion):
    ciclo = biblioteca.obtener_ciclo(red_canciones, cancion, n)
    imprimir.imprimir_flechas(ciclo)
    return


def rango(red_canciones, n, cancion):
    rango = biblioteca.rango_n(red_canciones, cancion, n)
    imprimir.imprimir_numero(rango)    


def clustering(red_canciones, cancion):
    if cancion:
        coef = biblioteca.calcular_clustering(red_canciones, cancion)
    else: 
        coef = biblioteca.clustering_promedio(red_canciones)
    coef = round(coef, 3)
    imprimir.imprimir_numero(coef)


def procesar_comando(comando, parametros, canciones_usuarios, canciones_por_playlist, usuarios, red_canciones, pagerank_ya_calculado):
    if comando == "camino":
        canciones = parametros.split(" >>>> ")
        camino(canciones_usuarios, canciones[0], canciones[1], usuarios)
    
    elif comando == "mas_importantes":
        mas_importantes(canciones_usuarios, usuarios, int(parametros), pagerank_ya_calculado)
    
    elif comando == "recomendacion":
        parametros_separados = parametros.split(" ", 2)
        tipo = parametros_separados[0]
        n = parametros_separados[1]
        canciones = parametros_separados[2].split(" >>>> ")
        cancion = random.choice(canciones)
        recomendacion(canciones_usuarios, cancion, tipo, usuarios, int(n))
    
    elif comando == "ciclo" or comando == "rango":
        es_ciclo = False
        if comando == "ciclo":
            es_ciclo = True
        parametros_separados = parametros.split(" ", 1)
        n = parametros_separados[0]
        cancion = parametros_separados[1]

        if es_ciclo:
            ciclo_n_canciones(red_canciones, int(n), cancion)
        else:
            rango(red_canciones, int(n) , cancion)

    elif comando == "clustering":
       clustering(red_canciones, parametros)





def procesar_entrada(canciones_usuarios, canciones_por_playlist, usuarios):
    esta_creado = False
    pagerank_ya_calculado = []
    red_canciones = None
    for row in sys.stdin:
        row = row.rstrip("\n")
        entrada = row.split(" ", 1)
        comando = entrada[0]
        if len(entrada) > 1:
            parametros = entrada[1]
        else:
            parametros = None

        if comando in ["ciclo", "rango", "clustering"] and not esta_creado:
            red_canciones = biblioteca.grafo_crear_estructura_2(canciones_por_playlist)
            esta_creado = True
        
        procesar_comando(comando, parametros, canciones_usuarios, canciones_por_playlist, usuarios, red_canciones, pagerank_ya_calculado)


        
def main():
    if len(sys.argv) != 2:
        return

    canciones_por_playlist, red_canciones_usuarios, usuarios = biblioteca.grafo_crear_estructura(sys.argv[1])

    procesar_entrada(red_canciones_usuarios, canciones_por_playlist, usuarios)

main()
