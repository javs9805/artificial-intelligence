from Estado import Estado
from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue

def BFS(estado_inicial, n):
    raiz = Estado(estado_inicial, None, None, 0, 0)
    if raiz.prueba():
        return raiz.solucion()
    frontera = Queue()
    frontera.put(raiz)
    explorado = []

    while not frontera.empty():
        nodo_actual = frontera.get()
        explorado.append(nodo_actual.estado)

        hijos = nodo_actual.expandir(n)
        for hijo in hijos:
            if hijo.estado not in explorado:
                if hijo.prueba():
                    return hijo.solucion(), len(explorado)
                frontera.put(hijo)
    return

def AStar_search(estado_inicial, n):
    frontera = PriorityQueue()
    explorado = []
    contador = 0
    raiz = Estado(estado_inicial, None, None, 0, 0)
    evaluacion = raiz.Distancia_Manhattan(n) 
    frontera.put((evaluacion[1], contador, raiz)) 

    while not frontera.empty():
        nodo_actual = frontera.get()
        nodo_actual = nodo_actual[2]
        explorado.append(nodo_actual.estado)

        if nodo_actual.prueba():
            return nodo_actual.solucion(), len(explorado)

        hijos = nodo_actual.expandir(n)
        for hijo in hijos:
            if hijo.estado not in explorado:
                contador += 1
                evaluacion = hijo.Distancia_Manhattan(n) 
                frontera.put((evaluacion[1], contador, hijo))
    return
