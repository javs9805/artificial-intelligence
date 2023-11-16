def leer_matriz_de_adyacencia(archivo):
    with open(archivo, 'r') as f:
        # Leer la cantidad de localidades
        cantidad_localidades = int(f.readline().strip())

        # Leer la matriz de adyacencia para el objetivo 1
        objetivo1 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]

        # Leer línea en blanco
        f.readline()

        # Leer la matriz de adyacencia para el objetivo 2
        objetivo2 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]

        # Leer línea en blanco
        f.readline()

        # Leer la matriz de adyacencia para las distancias
        distancias = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]

    return objetivo1, objetivo2, distancias

# Archivos de entrada
archivo_objetivo1 = 'qapUni.75.0.1.qap.txt'
archivo_objetivo2 = 'qapUni.75.p75.1.qap.txt'

# Obtener las matrices de adyacencia
objetivo1, objetivo2, distancias = leer_matriz_de_adyacencia(archivo_objetivo1)
print("Matriz de adyacencia para el objetivo 1:")
print(objetivo1)
print("Matriz de adyacencia para el objetivo 2:")
print(objetivo2)
print("Matriz de adyacencia para las distancias:")
print(distancias)


#NSGA
import random
def generar_individuo_aleatorio(cantidad_localidades):
    # Genera una permutación aleatoria de las localidades
    return random.sample(range(1, cantidad_localidades + 1), cantidad_localidades)

def generar_poblacion_inicial(cantidad_localidades, tamaño_poblacion):
    # Genera una población inicial de individuos aleatorios
    poblacion = []
    for _ in range(tamaño_poblacion):
        individuo = generar_individuo_aleatorio(cantidad_localidades)
        poblacion.append(individuo)
    return poblacion

# Lee la cantidad de localidades desde el archivo
archivo = 'qapUni.75.0.1.qap.txt'  # Puedes usar cualquiera de tus archivos
with open(archivo, 'r') as f:
    cantidad_localidades = int(f.readline().strip())

# Genera una población inicial aleatoria
tamaño_poblacion = 75  # Tamaño de la población, puedes ajustarlo según tus necesidades
poblacion_inicial = generar_poblacion_inicial(cantidad_localidades, tamaño_poblacion)

# Imprime la población inicial
print("Población Inicial:")
print(poblacion_inicial)

#################################################
def calcular_costo_asignacion(individuo, objetivo1, objetivo2, distancias):
    # Calcula el costo de asignación para un individuo dado
    costo_flujo = sum(objetivo1[i][individuo[i] - 1] for i in range(len(individuo)))
    costo_distancia = sum(objetivo2[i][individuo[i] - 1] for i in range(len(individuo)))
    costo_total = costo_flujo + costo_distancia
    return costo_total

def calcular_aptitud(poblacion, objetivo1, objetivo2, distancias):
    # Calcula el valor de aptitud para cada individuo en la población
    costo_total_poblacion = sum(calcular_costo_asignacion(individuo, objetivo1, objetivo2, distancias) for individuo in poblacion)
    aptitudes = [costo_total_poblacion / calcular_costo_asignacion(individuo, objetivo1, objetivo2, distancias) for individuo in poblacion]
    return aptitudes

# Ejemplo de uso
# Calcula el valor de aptitud para la población inicial
aptitudes = calcular_aptitud(poblacion_inicial, objetivo1, objetivo2, distancias)

# Imprime las aptitudes de la población inicial
print("Aptitudes de la población inicial:")
print(aptitudes)

#Un individuo con un menor costo de asignación tendrá un valor de aptitud más alto, indicando que es una mejor solución.


##########################################


def calcular_dominancia(individuo1, individuo2, objetivo1, objetivo2):
    domina = False
    if (objetivo1[individuo1] < objetivo1[individuo2] and objetivo2[individuo1] <= objetivo2[individuo2]) or \
       (objetivo1[individuo1] <= objetivo1[individuo2] and objetivo2[individuo1] < objetivo2[individuo2]):
        domina = True
    return domina

def calcular_frentes_pareto(poblacion, objetivo1, objetivo2):
    frentes = []
    dominancia = [0] * len(poblacion)
    dominados_por = [[] for _ in range(len(poblacion))]

    for i in range(len(poblacion)):
        for j in range(i+1, len(poblacion)):
            if calcular_dominancia(i, j, objetivo1, objetivo2):
                dominancia[j] += 1
                dominados_por[i].append(j)
            elif calcular_dominancia(j, i, objetivo1, objetivo2):
                dominancia[i] += 1
                dominados_por[j].append(i)

        if dominancia[i] == 0:
            frentes.append([i])

    idx_frente = 0
    while len(frentes[idx_frente]) > 0:
        siguiente_frente = []
        for i in frentes[idx_frente]:
            for j in dominados_por[i]:
                dominancia[j] -= 1
                if dominancia[j] == 0:
                    siguiente_frente.append(j)
        idx_frente += 1
        frentes.append(siguiente_frente)

    return frentes[:-1]  # Excluir el último frente vacío

# Ejemplo de uso
# Supongamos que tienes una población de soluciones llamada poblacion
# y matrices de adyacencia para los objetivos objetivo1 y objetivo2

# Calcular los frentes de Pareto
frentes_pareto = calcular_frentes_pareto(poblacion_inicial, objetivo1, objetivo2)

# Imprimir los frentes de Pareto
print("Frentes de Pareto:")
for i, frente in enumerate(frentes_pareto):
    print(f"Frente {i + 1}: {frente}")

########################################################
import matplotlib.pyplot as plt

def graficar_frentes_pareto(frentes_pareto, objetivo1, objetivo2):
    for i, frente in enumerate(frentes_pareto):
        x = [sum(objetivo1[individuo]) for individuo in frente]
        y = [sum(objetivo2[individuo]) for individuo in frente]

        # Unir los puntos del frente con líneas
        plt.plot(x, y, marker='o', label=f"Frente {i + 1}")

    plt.xlabel("Suma de Objetivo 1")
    plt.ylabel("Suma de Objetivo 2")
    plt.title("Frentes de Pareto")
    plt.legend()
    plt.show()

# Suponiendo que ya tienes los frentes_pareto, objetivo1 y objetivo2 definidos
graficar_frentes_pareto(frentes_pareto, objetivo1, objetivo2)


