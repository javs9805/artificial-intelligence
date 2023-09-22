
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
    
def MANHATTAN_DISTANCE(ESTADO_ACTUAL, MATRIZ_META):
    if len(ESTADO_ACTUAL) != len(MATRIZ_META) or len(ESTADO_ACTUAL[0]) != len(MATRIZ_META[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    distancia = 0

    for i in range(len(ESTADO_ACTUAL)):
        for j in range(len(ESTADO_ACTUAL[i])):
            valor_actual = ESTADO_ACTUAL[i][j]
            valor_meta = MATRIZ_META[i][j]
            distancia += abs(valor_actual - valor_meta)

    return distancia

def NRO_DE_PIEZAS_INCORRECTAS(ESTADO_ACTUAL, MATRIZ_META):
    if len(ESTADO_ACTUAL) != len(MATRIZ_META) or len(ESTADO_ACTUAL[0]) != len(MATRIZ_META[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    piezas_incorrectas = 0

    for i in range(len(ESTADO_ACTUAL)):
        for j in range(len(ESTADO_ACTUAL[i])):
            if ESTADO_ACTUAL[i][j] != MATRIZ_META[i][j]:
                piezas_incorrectas += 1

    return piezas_incorrectas

def GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta):
    # Inicializar el nodo inicial
    nodo_inicial = Nodo(
        parent=None,
        state=[],
        action=[],
        path_cost=0
    )

    # Calcular las heurísticas
    nodo_inicial.heuristic2 = NRO_DE_PIEZAS_INCORRECTAS(matriz_desordenada, matriz_meta)
    

    # Calcular los valores F1 y F2
    nodo_inicial.f2 = nodo_inicial.path_cost + nodo_inicial.heuristic2
   
    return nodo_inicial

# Crear el nodo inicial
nodo_inicial = GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta)

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




def obtener_NODO(open_list, estado):

    for tupla in open_list:
        segundo_elemento = tupla[1]
        if segundo_elemento == estado:
            tercer_elemento = tupla[2]
            return tercer_elemento
        
def obtener_COSTO(closet_list, estado):
    elemento_a_comparar = estado
    primer_elemento = None
    for x in closet_list:
         if x[1] == elemento_a_comparar:
             primer_elemento = x[0]
             return primer_elemento        

def eliminar_nodo_de_open_list(open_list, estado):    
    elemento_a_comparar = estado
# Crear una nueva lista sin la tupla que coincide
    open_list_sin_coincidencia = [(f2, state, nodo) for f2, state, nodo in open_list if state != elemento_a_comparar]

# Reemplazar open_list con la nueva lista
    open_list.clear()
    for tupla in open_list_sin_coincidencia:
        heapq.heappush(open_list, tupla)
    return open_list_sin_coincidencia 

def eliminar_nodo_de_closet_list(closed_list, estado):
    elemento_a_comparar = estado

# Convierte el conjunto de tuplas en una lista de tuplas
    closed_list_lista = [tuple(x) for x in closed_list]

# Elimina la tupla que coincide con el segundo elemento
    closed_list_lista = [tupla for tupla in closed_list_lista if tupla[1] != elemento_a_comparar]

# Convierte la lista de nuevo en un conjunto de tuplas
    closed_list = set(closed_list_lista)
    return closed_list


def A_START_F2(NODO_INICIAL, MATRIZ_DESORDENADA, MATRIZ_META):
    NODO_INICIAL.state = MATRIZ_DESORDENADA
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (NODO_INICIAL.f2, NODO_INICIAL.state, NODO_INICIAL))
    nodos_explorados = 0
    while open_list:
        costo_actual , estado, NODO = heapq.heappop(open_list)
        if son_matrices_iguales(estado, MATRIZ_META):
            print("Se llego a la meta")
            print("Nodos explorados:")
            print(nodos_explorados)
            return solucion(NODO)
            # Goal reached, construct and return the path

        closed_list.add((NODO.f2, tuple(map(tuple, NODO.state))))
        nodos_explorados = nodos_explorados +1
        ACCIONES = ACCIONES_LEGALES(estado)
        for ACCION in ACCIONES:
            # Crear NODO_HIJO
            NODO_HIJO = Nodo(
                parent=NODO,
                action=[ACCION],
                path_cost=NODO.path_cost + 1,
                state = CREAR_MATRIZ_TEMPORAL([ACCION] , NODO.state)
            )
            NODO_HIJO.heuristic2 = NRO_DE_PIEZAS_INCORRECTAS(NODO_HIJO.state, MATRIZ_META),
            NODO_HIJO.f2 = sum(NODO_HIJO.heuristic2) + NODO_HIJO.path_cost
            
            
            if any(nodo[1] == NODO_HIJO.state for nodo in open_list):
              
                   nodo_guardado = obtener_NODO(open_list, NODO_HIJO.state)
                   if nodo_guardado.f2 <= NODO_HIJO.f2:
                       continue
                   
                       
            if any(x[1] == NODO_HIJO.state for x in closed_list): 
                    costo =  obtener_COSTO(closed_list, NODO_HIJO.state)                                    
                    if costo <= NODO_HIJO.f2:
                        continue


nodo_inicial = GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta)
inicio_A_Start_F2 = time.time() 
CAMINO_A_START = A_START_F2(nodo_inicial,matriz_desordenada, matriz_meta)
fin_A_Start_F2 = time.time()
tiempo_transcurrido = fin_A_Start_F2 - inicio_A_Start_F2
print(tiempo_transcurrido)
