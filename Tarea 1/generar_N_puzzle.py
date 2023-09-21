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


with open("matrices.txt", "w") as archivo:
    archivo.write("Matriz Desordenada:\n")
    for fila in matriz_desordenada:
        archivo.write(" ".join(map(str, fila)) + "\n")
    archivo.write("\nMatriz Meta:\n")
    for fila in matriz_meta:
        archivo.write(" ".join(map(str, fila)) + "\n")   