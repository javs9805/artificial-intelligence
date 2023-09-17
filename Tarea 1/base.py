import random

def generar_tablero(N):
    tablero = list(range(1, N*N))
    tablero.append(0)  # Agregamos la casilla vacía representada por 0
    random.shuffle(tablero)
    return [tablero[i:i+N] for i in range(0, N*N, N)]

def imprimir_tablero(tablero):
    N = len(tablero)
    for i in range(N):
        for j in range(N):
            if tablero[i][j] == 0:
                print("  ", end=" ")
            else:
                print(f"{tablero[i][j]:2d}", end=" ")
        print()


"""
Ejemplo de uso funcion mover_pieza(tablero, movimiento):
tablero = generar_tablero(3)  # Cambia el tamaño del N-Puzzle según tus preferencias
imprimir_tablero(tablero)
mover_pieza(tablero, "arriba")
imprimir_tablero(tablero)
"""
def mover_pieza(tablero, movimiento):
    N = len(tablero)
    for i in range(N):
        for j in range(N):
            if tablero[i][j] == 0:  # Encontrar la casilla vacía
                if movimiento == "arriba" and i > 0:
                    tablero[i][j], tablero[i-1][j] = tablero[i-1][j], tablero[i][j]
                    return True
                elif movimiento == "abajo" and i < N-1:
                    tablero[i][j], tablero[i+1][j] = tablero[i+1][j], tablero[i][j]
                    return True
                elif movimiento == "izquierda" and j > 0:
                    tablero[i][j], tablero[i][j-1] = tablero[i][j-1], tablero[i][j]
                    return True
                elif movimiento == "derecha" and j < N-1:
                    tablero[i][j], tablero[i][j+1] = tablero[i][j+1], tablero[i][j]
                    return True
    return False  # Si el movimiento es inválido




def esta_resuelto(tablero):
    N = len(tablero)
    numero_esperado = 1

    for i in range(N):
        for j in range(N):
            if tablero[i][j] != numero_esperado:
                if numero_esperado != N*N:
                    return False
            numero_esperado += 1

    return True