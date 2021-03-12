import random

class Grafo:

    def __init__(self, es_dirigido):
        """Constructor. Recibe un parametro de tipo Bool indicando si es dirigido o no"""
        
        self.vertices = {}
        self.estado_es_dirigido = es_dirigido
        self.cantidad_aristas = 0
        self.cantidad_vertices = 0
    
    def __len__(self):
        """Devuelve la cantidad de vertices del grafo"""
        
        return self.cantidad_vertices

    def __iter__(self):
        """Itera todos los vertices del grafo"""
        
        return iter(self.vertices)

    def __str__(self):
        """Representacion del grafo como un diccionario de diccionarios"""
        
        return str(self.vertices)

    def agregar_vertice(self, clave):
        """Agrega un vertice al grafo. Si ya existia un vertice en el grafo con la misma clave devuelve False, True en caso contrario"""
        
        if clave in self.vertices:
           return False
        
        self.vertices[clave] = {}
        self.cantidad_vertices +=1
        return True
    
    def borrar_vertice(self, clave):
        """Borra un vertice del grafo y todas las aristas que lo conectan y devuelve True. En caso de que el vertice no se encuentre
         devuelve False"""
        
        if not clave in self.vertices: 
            return False

        self.vertices.pop(clave)
        for vertice in self.vertices:
            if clave in self.vertices[vertice]:
                self.vertices[vertice].pop(clave)
        return True

    def agregar_arista(self, inicio, fin, peso):
        """Agrega una arista al grafo que conecta los vertices pasados por parametro. En caso de que el grafo sea no pesado pasar como
        parametro None. En caso de agregarla correctamente devuelve True. 
        Si la clave de inicio o fin no se encuentra en el grafo o si el peso de la arista es 0 devuelve Falso"""
        
        if not inicio in self.vertices or not fin in self.vertices or self.estan_unidos(inicio, fin) or peso == 0 or inicio == fin:
           return False
     
        if peso == None:
            peso = 1
        
        self.vertices[inicio][fin] = peso

        if self.estado_es_dirigido == False:
            self.vertices[fin][inicio] = peso

        self.cantidad_aristas += 1
        return True

    def total_aristas(self): 
        """Devuelve la cantidad de aristas del grafo"""
        
        return self.cantidad_aristas

    def borrar_arista(self, inicio, fin):
        """Borra una arista del grafo en caso de que se haya borrado correctamente devuelve True. 
        En caso de que alguno los vertices pasados por parametro no pertenezcan al grafo devuelve False"""
        
        if not inicio in self.vertices or not fin in self.vertices:
           return False
        self.vertices[inicio].pop(fin)

        if self.estado_es_dirigido == False:
            self.vertices[fin].pop(inicio)
        return True

    def estan_unidos(self, inicio, fin):
        """Devuelve True si los vertices pasados por parametro estan unidos por una arista. En caso de que alguno de los vertices 
        o pertenezca al grafo devuelve False"""
        
        if not inicio in self.vertices or not fin in self.vertices:
           return False
        
        return fin in self.vertices[inicio]

    def peso_arista(self, inicio, fin):
        """Devuelve el peso de la arista que une a los vertices pasados por parametro y devuelve True. 
        En caso que alguno de los vertices no se encuentre en el grafo o estos no esten unidos devuelve False"""
        
        if not inicio in self.vertices or not fin in self.vertices or not self.estan_unidos(inicio, fin):
           return False

        return self.vertices[inicio][fin]
    
    def obtener_vertices(self):
        """Devuelve una lista con los vertices del grafo"""
        
        return self.vertices.keys()
    
    def adyacentes(self, vertice):
        """"Devuelve una lista con los vertices adyacentes del vertice pasado por parametro. En caso de que este no se encuentre en 
        el grafo devuelve una excepcion"""
        
        if not vertice in self.vertices:
            return None
        ady = list(self.vertices[vertice])
        return ady


    def vertice_aleatorio(self):
        """Devuelve un vertice aleatorio del grafo. En caso de que el grafo este vacio devuelve None"""
        if self.cantidad_vertices == 0:
            return None
        return random.choice(list(self.vertices.keys()))
