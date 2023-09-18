from algoritmosDeBusqueda import BFS, AStar_search
from time import time
import copy

# Estado inicial
n = int(input("Ingresa n\n"))
print("Ingresa tu puzzle", n, "*", n)
inicial = []
for i in range(0, n * n):
    p = int(input())
    inicial.append(p)

print("El estado dado es:", inicial)

# Contar el número de inversiones
def inv_num(puzzle):
    inv = 0
    for i in range(len(puzzle) - 1):
        for j in range(i + 1, len(puzzle)):
            if (puzzle[i] > puzzle[j] and puzzle[i] and puzzle[j]):
                inv += 1
    return inv

def es_solucionable(puzzle): # Comprobar si el estado inicial del puzzle es solucionable: el número de inversiones debe ser par.
    contador_inversiones = inv_num(puzzle)
    if (contador_inversiones % 2 == 0):
        return True
    return False

# Función para mover el espacio en blanco en el tablero
def mover_espacio_blanco(tablero, movimiento):
    indice_espacio_blanco = tablero.index(0)
    tamaño_tablero = n * n
    if movimiento == 'Arriba':
        if indice_espacio_blanco - n >= 0:
            tablero[indice_espacio_blanco], tablero[indice_espacio_blanco - n] = tablero[indice_espacio_blanco - n], tablero[indice_espacio_blanco]
    elif movimiento == 'Abajo':
        if indice_espacio_blanco + n < tamaño_tablero:
            tablero[indice_espacio_blanco], tablero[indice_espacio_blanco + n] = tablero[indice_espacio_blanco + n], tablero[indice_espacio_blanco]
    elif movimiento == 'Izquierda':
        if indice_espacio_blanco % n != 0:
            tablero[indice_espacio_blanco], tablero[indice_espacio_blanco - 1] = tablero[indice_espacio_blanco - 1], tablero[indice_espacio_blanco]
    elif movimiento == 'Derecha':
        if (indice_espacio_blanco + 1) % n != 0:
            tablero[indice_espacio_blanco], tablero[indice_espacio_blanco + 1] = tablero[indice_espacio_blanco + 1], tablero[indice_espacio_blanco]

def generar_estados_puzzle(movimientos, n, inicial):
    # Definir el estado inicial del tablero resuelto
    estado_inicial = inicial

    # Inicializar una lista para almacenar todas las situaciones del juego
    situaciones_puzzle = [estado_inicial]

    # Generar las situaciones del juego aplicando los movimientos
    for movimiento in movimientos:
        nuevo_estado = copy.copy(situaciones_puzzle[-1])
        mover_espacio_blanco(nuevo_estado, movimiento)
        situaciones_puzzle.append(nuevo_estado)

    return situaciones_puzzle

def mostrar_estados(movimientos, longitud, inicial):
    estados = generar_estados_puzzle(movimientos, longitud, inicial)
    for i, estado in enumerate(estados):
        print(f'Situación {i + 1}:')
        for j in range(0, len(estado), longitud):
            print(estado[j:j + longitud])
        print()

if es_solucionable(inicial):
    print("Solucionable, por favor espera. \n")

    time1 = time()
    solucion_BFS = BFS(inicial, n)
    tiempo_DFS = time() - time1
    print('Solución BFS es ', solucion_BFS[0])
    print('Número de nodos explorados es ', solucion_BFS[1])
    print('Tiempo BFS:', tiempo_DFS, "\n")
    mostrar_estados(solucion_BFS[0], n, inicial)

    time2 = time()
    solucion_AStar = AStar_search(inicial, n)
    tiempo_AStar = time() - time2
    print('Solución A* es ', solucion_AStar[0])
    print('Número de nodos explorados es ', solucion_AStar[1])
    print('Tiempo A*:', tiempo_AStar)
    mostrar_estados(solucion_AStar[0], n, inicial)
else:
    print("No solucionable")
