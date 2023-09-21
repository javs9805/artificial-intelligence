
import random
import copy
import time
from collections import deque
import heapq

def GENERAR_MATRIZ_META(N):
    if N < 2:
        raise ValueError("N debe ser igual o mayor que 2")

    matriz = [[0] * N for _ in range(N)]
    num = 1

    for i in range(N):
        for j in range(N):
            if num == N * N:
                matriz[N-1][N-1] = 0
                return matriz
            matriz[i][j] = num
            num += 1

    return matriz

# Ejemplo de uso
N = 3  # Puedes cambiar N al tamaño deseado del puzzle
matriz_meta = GENERAR_MATRIZ_META(N)
print("MATRIZ META")
for fila in matriz_meta:
    print(fila)


def GENERAR_MATRIZ_DESORDENADA_DESDE_META(MATRIZ_META, N):
    if N < 2:
        raise ValueError("N debe ser igual o mayor que 2")

    # Verificar si MATRIZ_META es válida
    if len(MATRIZ_META) != N or any(len(fila) != N for fila in MATRIZ_META):
        raise ValueError("MATRIZ_META no tiene la dimensión N x N")

    # Copiar la matriz ordenada para no modificarla
    matriz_desordenada = copy.deepcopy(MATRIZ_META)

    # Desordenar la matriz
    for _ in range(N * N * 2):
        movimientos_posibles = []
        x, y = None, None

        for i in range(N):
            for j in range(N):
                if matriz_desordenada[i][j] == 0:
                    x, y = i, j
                    break

        if x > 0:
            movimientos_posibles.append((x - 1, y))  # Mover hacia arriba
        if x < N - 1:
            movimientos_posibles.append((x + 1, y))  # Mover hacia abajo
        if y > 0:
            movimientos_posibles.append((x, y - 1))  # Mover hacia la izquierda
        if y < N - 1:
            movimientos_posibles.append((x, y + 1))  # Mover hacia la derecha

        nuevo_x, nuevo_y = random.choice(movimientos_posibles)
        matriz_desordenada[x][y], matriz_desordenada[nuevo_x][nuevo_y] = matriz_desordenada[nuevo_x][nuevo_y], matriz_desordenada[x][y]

    return matriz_desordenada

matriz_desordenada = GENERAR_MATRIZ_DESORDENADA_DESDE_META(matriz_meta, N)
print("DESORDENADA")
for fila in matriz_desordenada:
    print(fila)

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

distancia_de_Manhattan = MANHATTAN_DISTANCE(matriz_desordenada, matriz_meta)
print("Distancia de Manhattan ")
print(distancia_de_Manhattan)


def NRO_DE_PIEZAS_INCORRECTAS(ESTADO_ACTUAL, MATRIZ_META):
    if len(ESTADO_ACTUAL) != len(MATRIZ_META) or len(ESTADO_ACTUAL[0]) != len(MATRIZ_META[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    piezas_incorrectas = 0

    for i in range(len(ESTADO_ACTUAL)):
        for j in range(len(ESTADO_ACTUAL[i])):
            if ESTADO_ACTUAL[i][j] != MATRIZ_META[i][j]:
                piezas_incorrectas += 1

    return piezas_incorrectas

numero_piezas_incorrectas = NRO_DE_PIEZAS_INCORRECTAS(matriz_desordenada, matriz_meta)
print("Numero de piezas incorrectas:")
print(numero_piezas_incorrectas)

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

    # Calcular las heurísticas
    nodo_inicial.heuristic1 = MANHATTAN_DISTANCE(matriz_desordenada, matriz_meta)
    nodo_inicial.heuristic2 = NRO_DE_PIEZAS_INCORRECTAS(matriz_desordenada, matriz_meta)

    # Calcular los valores F1 y F2
    nodo_inicial.f1 = nodo_inicial.path_cost + nodo_inicial.heuristic1
    nodo_inicial.f2 = nodo_inicial.path_cost + nodo_inicial.heuristic2

    return nodo_inicial

# Crear el nodo inicial
nodo_inicial = GENERAR_NODO_INICIAL(matriz_desordenada, matriz_meta)



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


MATRIZ_TEMPORAL = CREAR_MATRIZ_TEMPORAL(nodo_inicial.state, matriz_desordenada)


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


def son_matrices_iguales(matriz1, matriz2):
    if len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0]):
        return False  # Las matrices tienen dimensiones diferentes

    for i in range(len(matriz1)):
        for j in range(len(matriz1[0])):
            if matriz1[i][j] != matriz2[i][j]:
                return False  # Elemento diferente encontrado

    return True  # Todas las comparaciones fueron iguales



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

def solucion(nodo_hoja):
    nodo_actual = nodo_hoja
    while nodo_actual.parent is not None:
        nodo_actual = nodo_actual.parent
    return nodo_actual



# Ahora, nodo_raíz contendrá el nodo raíz

   

# Llamamos a la función para obtener el camino desde la hoja hasta la raíz


# Ahora, nodo_raiz contendrá una lista de nodos desde la hoja hasta la raíz



def A_START_F1(NODO_INICIAL, MATRIZ_DESORDENADA, MATRIZ_META):
    NODO_INICIAL.state = MATRIZ_DESORDENADA
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (NODO_INICIAL.f1, NODO_INICIAL.state, NODO_INICIAL))
    nodos_explorados = 0
    while open_list:
        costo_actual , estado, NODO = heapq.heappop(open_list)
        if son_matrices_iguales(estado, MATRIZ_META):
            print("Se llego a la meta")
            print("Nodos explorados:")
            print(nodos_explorados)
            return solucion(NODO)
            # Goal reached, construct and return the path

        closed_list.add((NODO.f1, tuple(map(tuple, NODO.state))))
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
            NODO_HIJO.heuristic1 = MANHATTAN_DISTANCE(NODO_HIJO.state, MATRIZ_META),
            NODO_HIJO.f1 = sum(NODO_HIJO.heuristic1) + NODO_HIJO.path_cost
            
            
            if any(nodo[1] == NODO_HIJO.state for nodo in open_list):
              
                   nodo_guardado = obtener_NODO(open_list, NODO_HIJO.state)
                   if nodo_guardado.f1 <= NODO_HIJO.f1:
                       continue
                   
                       
            if any(x[1] == NODO_HIJO.state for x in closed_list): 
                    costo =  obtener_COSTO(closed_list, NODO_HIJO.state)                                    
                    if costo <= NODO_HIJO.f1:
                        continue
                
       
               
            open_list = eliminar_nodo_de_open_list(open_list, NODO_HIJO.state)
     
            closed_list = eliminar_nodo_de_closet_list(closed_list, NODO_HIJO.state)
            heapq.heappush(open_list, (NODO_HIJO.f1, NODO_HIJO.state, NODO_HIJO))

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
                
       
               
            open_list = eliminar_nodo_de_open_list(open_list, NODO_HIJO.state)
     
            closed_list = eliminar_nodo_de_closet_list(closed_list, NODO_HIJO.state)
            heapq.heappush(open_list, (NODO_HIJO.f2, NODO_HIJO.state, NODO_HIJO))
                                       
                
                


        

    



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
                
            else:
                print("YA SE EXPLORO")
    # Devolver NODO_INICIAL como la raíz del grafo
    print("Nodos explorados")
    print(nodos_explorados)
    return NODO_INICIAL
    

inicio_BFS = time.time() 
print("Matriz inicial")
print(matriz_desordenada)
print("Matriz meta")
print(matriz_meta)
RAIZ_ARBOL_BFS = BREADTH_FIRST_SEARCH(nodo_inicial, matriz_desordenada, matriz_meta)
fin_BFS = time.time()  # Marcar el tiempo de finalización
tiempo_transcurrido = fin_BFS - inicio_BFS

print(tiempo_transcurrido)

print("A* F1")
inicio_A_START = time.time()
RAIZ_ARBOL_A_F1 = A_START_F1(nodo_inicial, matriz_desordenada, matriz_meta)
fin_A_Start = time.time()
tiempo_transcurrido = fin_A_Start - inicio_A_START
print(tiempo_transcurrido) 
# Uso de la función para crear el árbol de búsqueda
#raiz_del_grafo = BREADTH_FIRST_SEARCH(nodo_inicial, matriz, matriz_meta)

# Llamar a la función de impresión a partir del nodo inicial
print("A* F2")
print("Matriz desordenada")
print(matriz_desordenada)
print("Matriz ordenada")
print(matriz_meta)
RAIZ_ARBOL_A_F2 = A_START_F2(nodo_inicial, matriz_desordenada, matriz_meta)







