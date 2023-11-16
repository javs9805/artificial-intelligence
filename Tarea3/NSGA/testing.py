import random
import matplotlib.pyplot as plt
import numpy as np 

def leer_matriz_de_adyacencia(archivo):
    with open(archivo, 'r') as f:
        cantidad_localidades = int(f.readline().strip())
        objetivo1 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]
        f.readline()  # Leer línea en blanco
        objetivo2 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]
        f.readline()  # Leer línea en blanco
        distancias = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]

    return objetivo1, objetivo2, distancias

def generar_individuo_aleatorio(cantidad_localidades):
    secuencia = list(range(1, cantidad_localidades + 1))
    random.shuffle(secuencia)
    return secuencia

def generar_poblacion_inicial(cantidad_localidades, tamano_poblacion):
    return [generar_individuo_aleatorio(cantidad_localidades) for _ in range(tamano_poblacion)]

def calcular_costo_asignacion(individuo, objetivo):
    return sum(objetivo[i][individuo[i] - 1] for i in range(len(individuo)))

def calcular_frente_pareto(poblacion, objetivo1, objetivo2):
    frentes_pareto = []
    soluciones_no_pareto = list(range(len(poblacion)))

    while soluciones_no_pareto:
        frente_actual = []
        for solucion in soluciones_no_pareto[:]:
            domina = False
            for solucion_comparar in soluciones_no_pareto[:]:
                if solucion != solucion_comparar:
                    costo_solucion = [calcular_costo_asignacion(poblacion[solucion], objetivo1),
                                      calcular_costo_asignacion(poblacion[solucion], objetivo2)]
                    costo_comparar = [calcular_costo_asignacion(poblacion[solucion_comparar], objetivo1),
                                       calcular_costo_asignacion(poblacion[solucion_comparar], objetivo2)]

                    if all(costo_solucion[i] <= costo_comparar[i] for i in range(2)) and \
                       any(costo_solucion[i] < costo_comparar[i] for i in range(2)):
                        domina = True
                        break

            if not domina:
                frente_actual.append(solucion)
                soluciones_no_pareto.remove(solucion)

        frentes_pareto.append(frente_actual)

    return frentes_pareto


import numpy as np

def calcular_distancia_crowding(frente, objetivo1, objetivo2):
    num_soluciones = len(frente)

    # Inicializar la distancia crowding
    distancia_crowding = [0] * num_soluciones

    for i in range(len(objetivo1[0])):
        # Obtener los valores objetivo para el objetivo actual
        valores_objetivo = [objetivo1[j][i] + objetivo2[j][i] for j in frente]

        # Obtener los índices ordenados de las soluciones en el frente
        frente_ordenado = sorted(range(num_soluciones), key=lambda k: valores_objetivo[k])

        # Calcular la distancia crowding
        distancia_crowding[frente_ordenado[0]] = np.inf
        distancia_crowding[frente_ordenado[-1]] = np.inf
        for j in range(1, num_soluciones - 1):
            distancia_crowding[frente_ordenado[j]] += (valores_objetivo[frente_ordenado[j + 1]] - valores_objetivo[frente_ordenado[j - 1]])

    return distancia_crowding

# Utiliza esta función en tu código principal.

# Luego, podrías usar esta función en tu código existente.

# Luego, podrías usar esta función en tu código existente.


def ordenar_frentes_pareto(frentes_pareto, objetivo1, objetivo2):
    frentes_ordenados = []
    for frente in frentes_pareto:
        distancia_crowding = calcular_distancia_crowding(frente, objetivo1, objetivo2)
        frente_ordenado = sorted(range(len(frente)), key=lambda x: distancia_crowding[x], reverse=True)
        frentes_ordenados.append([frente[i] for i in frente_ordenado])
    return frentes_ordenados

def graficar_frentes_pareto(frentes_pareto, objetivo1, objetivo2):
    frentes_ordenados = ordenar_frentes_pareto(frentes_pareto, objetivo1, objetivo2)

    for i, frente in enumerate(frentes_ordenados):
        x = [sum(objetivo1[individuo]) for individuo in frente]
        y = [sum(objetivo2[individuo]) for individuo in frente]

        # Unir los puntos del frente con líneas
        plt.plot(x, y, marker='o', label=f"Frente {i + 1}")

    plt.xlabel("Suma de Objetivo 1")
    plt.ylabel("Suma de Objetivo 2")
    plt.title("Frentes de Pareto")
    plt.legend()
    plt.show()

# Ejemplo de uso
archivo_objetivo1 = 'qapUni.75.0.1.qap.txt'
archivo_objetivo2 = 'qapUni.75.p75.1.qap.txt'
objetivo1, objetivo2, distancias = leer_matriz_de_adyacencia(archivo_objetivo1)

tamano_poblacion = 10
poblacion_inicial = generar_poblacion_inicial(len(objetivo1), tamano_poblacion)

frentes_pareto = calcular_frente_pareto(poblacion_inicial, objetivo1, objetivo2)

# Graficar los frentes de Pareto
graficar_frentes_pareto(frentes_pareto, objetivo1, objetivo2)
