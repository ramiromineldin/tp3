import random

class Grafo:

    def __init__(self, es_dirigido):
        self.vertices = {}
        self.estado_es_dirigido = es_dirigido
    
    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __str__(self):
        return str(self.vertices)

    def agregar_vertice(self, clave):
        if clave in self.vertices:
           return False
        
        self.vertices[clave] = {}
        return True
    
    def borrar_vertice(self, clave):
        if not clave in self.vertices: 
            return False

        self.vertices.pop(clave)
        for vertice in self.vertices:
            if clave in self.vertices[vertice]:
                self.vertices[vertice].pop(clave)
        return True

    def agregar_arista(self, inicio, fin, peso):
        if not inicio in self.vertices or not fin in self.vertices:
           return False

        if peso == None:
            peso = 1
        
        self.vertices[inicio][fin] = peso

        if self.estado_es_dirigido == False:
            self.vertices[fin][inicio] = peso
        return True

    def borrar_arista(self, inicio, fin):
        if not inicio in self.vertices or not fin in self.vertices:
           return False
        self.vertices[inicio].pop(fin)

        if self.estado_es_dirigido == False:
            self.vertices[fin].pop(inicio)
        return True

    def estan_unidos(self, inicio, fin):
        if not inicio in self.vertices or not fin in self.vertices:
           return False
        
        return fin in self.vertices[inicio]

    def peso_arista(self, inicio, fin):
        if not inicio in self.vertices or not fin in self.vertices:
           return False

        return self.vertices[inicio][fin]
    
    def obtener_vertices(self):
        return self.vertices.keys()
    
    def adyacentes(self, vertice):
        if not vertice in self.vertices:
            return False
        ady = list(self.vertices[vertice])
        return ady


    def vertice_aleatorio(self):
        return random.choice(list(self.vertices.keys()))

