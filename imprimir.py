def imprimir_camino(lista):
    """Recibe una lista e imprime los elementos de esta separada por flechas y las distantas frases"""
    
    frases = {0: "aparece en playlist", 1: "de", 2: "tiene una playlist", 3: "donde aparece"}
    a_imprimir = []
    num_frase = 0
    largo = 0
    while largo < len(lista):
        a_imprimir.append(lista[largo])
        a_imprimir.append(" --> ")
        if (largo < len(lista) - 1):
            a_imprimir.append(frases[num_frase])
            a_imprimir.append(" --> ")
            num_frase+=1

        if num_frase > len(frases) - 1:
            num_frase = 0
        largo+=1
    
    a_imprimir.pop()
    print(''.join(a_imprimir))


def imprimir_flechas(lista):
    """Recibe una lista e imprime los elementos de esta separada por flechas"""
    
    print(" --> ".join(lista))

def imprimir_puntocoma(lista):
    """Recibe una lista e imprime los elementos de esta separada por punto y coma"""
    
    print("; ".join(lista))

def imprimir_dato(dato): 
    """Recibe un dato y lo imprime"""
    
    print(dato)
