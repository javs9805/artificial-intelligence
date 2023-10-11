
import random
import copy
import time
from collections import deque
import heapq

n = 3  # Tamaño de la matriz (ajusta esto según tus necesidades)

matriz_desordenada = []
matriz_meta = []

with open("matrices.txt", "r") as archivo:
    leyendo_matriz_desordenada = False  # Variable para rastrear si estamos leyendo la matriz desordenada o la meta

    for linea in archivo:
        linea = linea.strip()  # Elimina espacios en blanco al inicio y al final

        if not linea:  # Si la línea está en blanco, omitirla
            continue

        if linea == "Matriz Desordenada:":
            leyendo_matriz_desordenada = True
            continue  # Salta esta línea
        elif linea == "Matriz Meta:":
            leyendo_matriz_desordenada = False
            continue  # Salta esta línea

        numeros = list(map(int, linea.split()))

        if leyendo_matriz_desordenada:
            matriz_desordenada.append(numeros)
        else:
            matriz_meta.append(numeros)

# Ahora, matriz_desordenada y matriz_meta contienen las matrices leídas desde el archivo
class Nodo:
    def __init__(self, parent=None, state=None, action=None, path_cost=0):
        self.parent = parent  # Puntero al nodo padre
        self.state = state  # Lista de acciones
        self.action = action  # Acción que llevó a este nodo desde el padre
        self.path_cost = path_cost  # Costo acumulado desde el nodo inicial
        self.heuristic1 = None  # Heurística 1 (distancia de Manhattan)
        self.heuristic2 = None  # Heurística 2 (número de piezas incorrectas)
        self.f1 = None  # Valor F1 (path_cost + heuristic1)
        self.f2 = None  # Valor F2 (path_cost + heuristic2)
        self.children = []
    def __lt__(self, other):
        return self.f1 < other.f1
        

def GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta):
    # Inicializar el nodo inicial
    nodo_inicial = Nodo(
        parent=None,
        state=[],
        action=[],
        path_cost=0
    )


    return nodo_inicial


def son_matrices_iguales(matriz1, matriz2):
    if len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0]):
        return False  # Las matrices tienen dimensiones diferentes

    for i in range(len(matriz1)):
        for j in range(len(matriz1[0])):
            if matriz1[i][j] != matriz2[i][j]:
                return False  # Elemento diferente encontrado

    return True  # Todas las comparaciones fueron iguales

def solucion(nodo_hoja):
    camino = []  # Aquí almacenaremos el camino desde la hoja hasta la raíz

    nodo_actual = nodo_hoja
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = nodo_actual.parent
    return camino

def BUSCAR_ESPACIO_BLANCO(MATRIZ_TEMPORAL):
    # Buscar la posición del espacio en blanco (valor 0) en la matriz
    for i in range(len(MATRIZ_TEMPORAL)):
        for j in range(len(MATRIZ_TEMPORAL[i])):
            if MATRIZ_TEMPORAL[i][j] == 0:
                return i, j  # Devolver las coordenadas del espacio en blanco

def ACCIONES_LEGALES(MATRIZ_TEMPORAL):
    # Obtener las coordenadas del espacio en blanco
    i, j = BUSCAR_ESPACIO_BLANCO(MATRIZ_TEMPORAL)

    # Definir las acciones posibles
    acciones_posibles = []

    # Verificar si se pueden realizar las acciones y agregarlas a la lista de acciones posibles
    if j < len(MATRIZ_TEMPORAL[0]) - 1:
        acciones_posibles.append("DERECHA")
    if j > 0:
        acciones_posibles.append("IZQUIERDA")
    if i > 0:
        acciones_posibles.append("ARRIBA")
    if i < len(MATRIZ_TEMPORAL) - 1:
        acciones_posibles.append("ABAJO")

    return acciones_posibles

def CREAR_MATRIZ_TEMPORAL(ACCIONES, MATRIZ_DESORDENADA):
    # Crear una copia de la matriz desordenada
    MATRIZ_RESULTANTE = [list(row) for row in MATRIZ_DESORDENADA]

    for accion in ACCIONES:
        # Buscar la posición del espacio en blanco (valor 0) en la matriz resultante
        for i in range(len(MATRIZ_RESULTANTE)):
            for j in range(len(MATRIZ_RESULTANTE[i])):
                if MATRIZ_RESULTANTE[i][j] == 0:
                    x, y = i, j
                    break

        # Realizar la acción especificada
        if accion == "DERECHA" and y < len(MATRIZ_RESULTANTE[0]) - 1:
            MATRIZ_RESULTANTE[x][y], MATRIZ_RESULTANTE[x][y + 1] = MATRIZ_RESULTANTE[x][y + 1], MATRIZ_RESULTANTE[x][y]
        elif accion == "IZQUIERDA" and y > 0:
            MATRIZ_RESULTANTE[x][y], MATRIZ_RESULTANTE[x][y - 1] = MATRIZ_RESULTANTE[x][y - 1], MATRIZ_RESULTANTE[x][y]
        elif accion == "ARRIBA" and x > 0:
            MATRIZ_RESULTANTE[x][y], MATRIZ_RESULTANTE[x - 1][y] = MATRIZ_RESULTANTE[x - 1][y], MATRIZ_RESULTANTE[x][y]
        elif accion == "ABAJO" and x < len(MATRIZ_RESULTANTE) - 1:
            MATRIZ_RESULTANTE[x][y], MATRIZ_RESULTANTE[x + 1][y] = MATRIZ_RESULTANTE[x + 1][y], MATRIZ_RESULTANTE[x][y]

    return MATRIZ_RESULTANTE


failure= []
def BREADTH_FIRST_SEARCH(NODO_INICIAL, MATRIZ_DESORDENADA, MATRIZ_META):
    print("BFS")
    # Crear cola Q
    Q = deque()
    nodos_explorados =1
    NODO_INICIAL.state = MATRIZ_DESORDENADA
    # Agregar NODO_INICIAL en cola Q
    Q.append(NODO_INICIAL)
    estados_explorados = set()
    estados_explorados.add(tuple(map(tuple, NODO_INICIAL.state)))
    # Mientras Q no esté vacía:
    while Q:
        # Quitar elemento de Q
        NODO = Q.popleft()
        # Crear MATRIZ_TEMPORAL
        # Obtener ACCIONES legales
        ESTADO_ACTUAL = NODO.state
      
        if son_matrices_iguales(ESTADO_ACTUAL, MATRIZ_META):
            print("Se llego a la meta")
            print("Nodos explorados")
            print(nodos_explorados)
            return solucion(NODO)
            
        ACCIONES = ACCIONES_LEGALES(NODO.state)
        # Para cada ACCION de ACCIONES:
        for ACCION in ACCIONES:
            # Crear NODO_HIJO
            NODO_HIJO = Nodo(
                parent=NODO,
                action=[ACCION],
                path_cost=NODO.path_cost + 1,
                state = CREAR_MATRIZ_TEMPORAL([ACCION] , ESTADO_ACTUAL)
            )
          
            if tuple(map(tuple, NODO_HIJO.state)) not in estados_explorados:
                nodos_explorados = nodos_explorados+1
        
                estados_explorados.add(tuple(map(tuple, NODO_HIJO.state)))
              
                 # Colocar NODO_HIJO en Q
                Q.append(NODO_HIJO)
                 # Agregar NODO_HIJO como hijo del nodo actual
                NODO.children.append(NODO_HIJO)  # Asumiendo que el nodo tiene un atributo 'children' para almacenar a sus hijos
                 # Imprimir NODO_HIJO.state
                
            
    # Devolver NODO_INICIAL como la raíz del grafo
    return failure  


def generarMatrizOrdenada(N):
    # Crea una lista con los números del 1 a (NxN)-1
    numeros = list(range(1, N * N))
    print(numeros)
    numeros.append(0)
    # Crea una matriz NxN llena de ceros
    tabla = [[0] * N for _ in range(N)]

    # Llena la matriz con los números del 1 a (NxN)-1
    for i in range(N):
        for j in range(N):
            tabla[i][j] = numeros.pop(0)

    # Deja el elemento NxN (última fila y última columna) vacío
    tabla[N - 1][N - 1] = 0

    return tabla    

def iniciarSolucion(matriz_desordenada,N):
    matriz_meta = generarMatrizOrdenada(N)
    nodo_inicial = GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta)

    inicio_BFS = time.time() 
    print("matriz desordenada")
    print(matriz_desordenada)
    print("matriz meta")
    print(matriz_meta)
    RAIZ_ARBOL_BFS = BREADTH_FIRST_SEARCH(nodo_inicial, matriz_desordenada, matriz_meta)
    fin_BFS = time.time()  # Marcar el tiempo de finalización
    tiempo_transcurrido = fin_BFS - inicio_BFS
    print(RAIZ_ARBOL_BFS)
    print("Tiempo transcurrido:")
    print(tiempo_transcurrido)
    return RAIZ_ARBOL_BFS

