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
tamaño_poblacion = 10  # Tamaño de la población, puedes ajustarlo según tus necesidades
poblacion_inicial = generar_poblacion_inicial(cantidad_localidades, tamaño_poblacion)

# Imprime la población inicial
print("Población Inicial:")
print(poblacion_inicial)

import random

def generar_poblacion_inicial(cantidad_localidades, tamaño_poblacion):
    poblacion = []
    for _ in range(tamaño_poblacion):
        individuo = generar_individuo_aleatorio(cantidad_localidades)
        poblacion.append(individuo)
    return poblacion

def calcular_dominancia(individuo1, individuo2, objetivo1, objetivo2):
    domina = False
    if (objetivo1[individuo1] < objetivo1[individuo2] and objetivo2[individuo1] <= objetivo2[individuo2]) or \
       (objetivo1[individuo1] <= objetivo1[individuo2] and objetivo2[individuo1] < objetivo2[individuo2]):
        domina = True
    return domina

def calcular_frentes_pareto(poblacion, objetivo1, objetivo2):
    dominancia = [0] * len(poblacion)
    dominados_por = [[] for _ in range(len(poblacion))]
    frentes_pareto = []

    for i in range(len(poblacion)):
        for j in range(i+1, len(poblacion)):
            if calcular_dominancia(i, j, objetivo1, objetivo2):
                dominancia[j] += 1
                dominados_por[i].append(j)
            elif calcular_dominancia(j, i, objetivo1, objetivo2):
                dominancia[i] += 1
                dominados_por[j].append(i)

        if dominancia[i] == 0:
            frentes_pareto.append([i])

    idx_frente = 0
    while len(frentes_pareto[idx_frente]) > 0:
        siguiente_frente = []
        for i in frentes_pareto[idx_frente]:
            for j in dominados_por[i]:
                dominancia[j] -= 1
                if dominancia[j] == 0:
                    siguiente_frente.append(j)
        idx_frente += 1
        frentes_pareto.append(siguiente_frente)

    return frentes_pareto[:-1]  # Excluir el último frente vacío

# Ejemplo de uso
cantidad_localidades = 10  # Ajusta según tus necesidades
tamaño_poblacion = 100
objetivo1 = [random.random() for _ in range(tamaño_poblacion)]
objetivo2 = [random.random() for _ in range(tamaño_poblacion)]

poblacion = generar_poblacion_inicial(cantidad_localidades, tamaño_poblacion)
frentes_pareto = calcular_frentes_pareto(poblacion, objetivo1, objetivo2)

# Imprimir los frentes de Pareto
print("Frentes de Pareto:")
for i, frente in enumerate(frentes_pareto):
    print(f"Frente {i + 1}: {frente}")




