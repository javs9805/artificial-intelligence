import numpy as np

def distancia_euclidiana(p, q):
    return np.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q)))

def metrica_M1(Y_aprox, Y_true):
    if not Y_aprox:
        return 0

    suma_distancias = 0

    for punto_aprox in Y_aprox:
        distancia_minima = min(distancia_euclidiana(punto_aprox, punto_true) for punto_true in Y_true)
        suma_distancias += distancia_minima

    return 1 / len(Y_aprox) * suma_distancias

# Ejemplo de uso:
Y_true = [[1, 2], [3, 4], [5, 6]]
Y_aprox = [[2, 3], [4, 5]]

m1_resultado = metrica_M1(Y_aprox, Y_true)
print("M1' =", m1_resultado)
