import random
import matplotlib.pyplot as plt
import numpy as np 
import json




def leer_matriz_de_adyacencia(archivo):
    with open(archivo, 'r') as f:
        cantidad_localidades = int(f.readline().strip())
        objetivo1 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]
        f.readline()  # Leer línea en blanco
        objetivo2 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]
        f.readline()  # Leer línea en blanco
        distancias = [[int(valor) for valor in f.readline().strip().split()] for _ in range(cantidad_localidades)]

    return objetivo1, objetivo2, distancias, cantidad_localidades

def generar_individuo_aleatorio(cantidad_localidades):
    secuencia = list(range(0, cantidad_localidades ))
    random.shuffle(secuencia)
    return secuencia

def generar_poblacion_inicial(cantidad_localidades, tamano_poblacion):
    return [generar_individuo_aleatorio(cantidad_localidades) for _ in range(tamano_poblacion)]


def calcular_costo_asignacion(individuo, objetivo):
    return sum(objetivo[i][individuo[i] - 1] for i in range(len(individuo)))




# Ejemplo de uso
# Supongamos que tienes una población de soluciones llamada poblacion_inicial
# y matrices de adyacencia para los objetivos objetivo1 y objetivo2

# Calcular los frentes de Pareto

# Imprimir los frentes de Pareto



def calcular_asignacion_de_costo(cromosoma,distancia,flujo):
    costo = 0    
    for x in range(0, len(cromosoma)):
        for y in range (x, len(cromosoma)):
            costo = distancia[x][y]*flujo[cromosoma[x]][cromosoma[y]] + costo    
    return costo


def calcular_funcion_objetivo(poblacion_inicial, distancia, flujo):
    funcion_objetivo = []
    for i in range(0,len(poblacion_inicial)):
        funcion_objetivo.append(calcular_asignacion_de_costo(poblacion_inicial[i], distancia, flujo))
    return funcion_objetivo


def solucionB_domina(solucion_A, solucion_B):
    objetivo_A1, objetivo_A2 = solucion_A
    objetivo_B1, objetivo_B2 = solucion_B

    # B domina a A si es al menos tan bueno en ambos objetivos y mejor en al menos uno
    return (objetivo_B1 <= objetivo_A1 and objetivo_B2 <= objetivo_A2) and \
           (objetivo_B1 < objetivo_A1 or objetivo_B2 < objetivo_A2)


def es_no_dominado(solucion_A, soluciones):
    no_dominado = True
    for j, solucion_B in enumerate(soluciones):
        if solucionB_domina(solucion_A, solucion_B):
            no_dominado = False
            break
    return no_dominado 

# Nota: Esto imprimirá las relaciones de dominancia entre todas las combinaciones de soluciones en la lista.




def calcular_ranking_frentes_pareto(poblacion_inicial):
    poblacion = poblacion_inicial
    ranking_pareto = []
    while poblacion:
        frente_pareto = []
        for i, individuo in enumerate(poblacion):
            print(individuo)
            if es_no_dominado(individuo,poblacion):
                frente_pareto.append(individuo) 

        ranking_pareto.append(frente_pareto)
        poblacion = [individuo for individuo in poblacion if individuo not in frente_pareto]

    return ranking_pareto
        


def graficar_frentes(ranking_pareto, color_lines=True):
    for i, frente in enumerate(ranking_pareto):
        x = [solucion[0] for solucion in frente]
        y = [solucion[1] for solucion in frente]

        # Obtener el color correspondiente al frente
        color = plt.cm.viridis(i / len(ranking_pareto))

        # Scatter plot para los puntos
        plt.scatter(x, y, label=f'Frente {i + 1}', color=color)

        # Ordenar los puntos por distancia euclidiana
        puntos_ordenados = np.array(sorted(zip(x, y), key=lambda punto: punto[0]))

        # Line plot para unir los puntos del mismo frente
        for j in range(len(puntos_ordenados) - 1):
            if color_lines:
                plt.plot([puntos_ordenados[j][0], puntos_ordenados[j+1][0]],
                         [puntos_ordenados[j][1], puntos_ordenados[j+1][1]],
                         color=color, linestyle='-', linewidth=1)

    plt.xlabel('Objetivo 1')
    plt.ylabel('Objetivo 2')
    plt.title('Frentes de Pareto')
    plt.legend()
    plt.show()



def calcular_dummy_fitness_con_sharing(ranking_pareto, funcion_1_2):
    dummy_fitness_con_sharing = []
    cantidad_frentes = len(ranking_pareto)
    for idx_lista, lista_pareto in enumerate(ranking_pareto):
        for tupla_funcion in funcion_1_2:
            if tupla_funcion in lista_pareto:
                print(f'Elemento {tupla_funcion} encontrado en la lista de Pareto en la posición {idx_lista}')
                cantidad_elementos = len(lista_pareto)
                print(f'Frente numero {idx_lista+1}')
                print(f'Cantidad de elementos {cantidad_elementos}')
                nro_frente = idx_lista + 1
                dummy_fitness = cantidad_frentes/nro_frente
                sharing = dummy_fitness/cantidad_elementos
                dummy_fitness_con_sharing.append(sharing)
    return dummy_fitness_con_sharing



##Seleccion de Padres
#Torneo binario

def binary_tournament_selection(population, fitness_values):
    # Seleccionar dos individuos al azar
    index1, index2 = random.sample(range(len(population)), 2)
    
    # Comparar sus valores de dummy fitness
    fitness1 = fitness_values[index1]
    fitness2 = fitness_values[index2]
    
    # Seleccionar al individuo con el menor valor de dummy fitness
    if fitness1 < fitness2:
        return population[index1]
    else:
        return population[index2]
    


"""
print("Frentes de Pareto:")
for i, frente in enumerate(frentes_pareto):
    print(f"Frente {i + 1}: {frente}")
"""
####Crossover y mutacion

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(individual, mutation_rate):
    mutated_individual = list(individual)
    if random.uniform(0, 1) < mutation_rate:
        mutation_point = random.randint(0, len(mutated_individual) - 2)
        mutated_individual[mutation_point], mutated_individual[mutation_point + 1] = \
            mutated_individual[mutation_point + 1], mutated_individual[mutation_point]
    return mutated_individual

# Parámetros



def crossover_mutation(poblacion, dummy_fitness_con_sharing, tasa_mutacion):
    # Realizar crossover para generar nueva población
    nueva_poblacion = []
    for i in range(0, len(poblacion), 2):
        padre1 = binary_tournament_selection(poblacion, dummy_fitness_con_sharing)
        padre2 = binary_tournament_selection(poblacion, dummy_fitness_con_sharing)
        descendiente1, descendiente2 = crossover(padre1, padre2)
        nueva_poblacion.extend([descendiente1, descendiente2])

    # Aplicar mutación al 10% de la población generada mediante crossover
    indice_mutation = random.sample(range(len(nueva_poblacion)), int(0.1 * len(nueva_poblacion)))
    for i in indice_mutation:
     nueva_poblacion[i] = mutation(nueva_poblacion[i], tasa_mutacion)

    print("Tamaño de la nueva poblacion")
    print(len(nueva_poblacion))
    # Ahora, la población resultante después de crossover y mutación está en 'nueva_poblacion'
    return nueva_poblacion



archivo_objetivo1 = 'qapUni.75.0.1.qap.txt'
archivo_objetivo2 = 'qapUni.75.p75.1.qap.txt'
objetivo1, objetivo2, distancias, cantidad_localidades = leer_matriz_de_adyacencia(archivo_objetivo1)

tamano_poblacion = 70
poblacion_inicial = generar_poblacion_inicial(cantidad_localidades, tamano_poblacion)
# Assuming the previous code for initialization and the first generation

# Number of generations
num_generations = 100

for generation in range(1, num_generations + 1):
    # Perform genetic operations on the current population
    funcion_objetivo_1 = calcular_funcion_objetivo(poblacion_inicial, distancias, objetivo1)
    funcion_objetivo_2 = calcular_funcion_objetivo(poblacion_inicial, distancias, objetivo2)
    funcion_1_2 = list(zip(funcion_objetivo_1, funcion_objetivo_2))
    
    ranking_pareto = calcular_ranking_frentes_pareto(funcion_1_2)
    #graficar_frentes(ranking_pareto)
    
    dummy_fitness_con_sharing = calcular_dummy_fitness_con_sharing(ranking_pareto, funcion_1_2)
    
    tasa_mutacion = 0.1
    nueva_poblacion = crossover_mutation(poblacion_inicial, dummy_fitness_con_sharing, tasa_mutacion)
    
    # Update the current population with the new one
    poblacion_inicial = nueva_poblacion
    
    # Print information about the current generation
    print(f"Generation {generation} - Pareto Fronts: {len(ranking_pareto)}")

pareto_optimo = ranking_pareto[0]
nombre_archivo = "pareto_optimo.json"
with open(nombre_archivo, 'a') as archivo:
    # Agregar la primera lista al final del archivo
    archivo.write(json.dumps(pareto_optimo) + '\n')
# After the loop, you can analyze the final Pareto fronts or the last population as needed
#graficar_frentes(ranking_pareto)


import json

pareto_optimo = ranking_pareto[0]
nombre_archivo = "pareto_optimo.json"
with open(nombre_archivo, 'a') as archivo:
    # Agregar la primera lista al final del archivo
    archivo.write(json.dumps(pareto_optimo) + '\n')

import json
# Lee el archivo JSON línea por línea
frentes_pareto_data = []
with open('pareto_optimo.json', 'r') as file:
    for line in file:
        frente = json.loads(line)
        frentes_pareto_data.append(frente)

# Inicializa el mejor frente Pareto y su hipervolumen
mejor_frente = None
mejor_hipervolumen = float('-inf')

# Itera sobre los frentes obtenidos
for frente in frentes_pareto_data:
    # Calcula el hipervolumen como el producto de las coordenadas de cada punto
    hipervolumen = sum(punto[0] * punto[1] for punto in frente)
    
    # Actualiza el mejor frente si el hipervolumen es mayor
    if hipervolumen > mejor_hipervolumen:
        mejor_hipervolumen = hipervolumen
        mejor_frente = frente

# Imprime el mejor frente Pareto y su hipervolumen
print("Mejor Frente Pareto:")
print(mejor_frente)
print("Hipervolumen:", mejor_hipervolumen)

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

def distancia_euclidiana(p, q):
    return np.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q)))

def calcular_W(punto_aprox, Y_true, epsilon):
    return [punto_true for punto_true in Y_true if distancia_euclidiana(punto_aprox, punto_true) <= epsilon]

def metrica_M2(Y_aprox, Y_true, epsilon):
    if not Y_aprox:
        return 0

    suma_tamanos_W = 0

    for punto_aprox in Y_aprox:
        W = calcular_W(punto_aprox, Y_true, epsilon)
        suma_tamanos_W += len(W)

    return 1 / (len(Y_aprox) - 1) * suma_tamanos_W

def metrica_M3(Y_aprox):
    if not Y_aprox:
        return 0

    distancia_maxima = 0

    for i in range(len(Y_aprox)):
        for j in range(i + 1, len(Y_aprox)):
            distancia_maxima = max(distancia_maxima, distancia_euclidiana(Y_aprox[i], Y_aprox[j]))

    return distancia_maxima

def calcular_metrica_error(Y_aprox, Y_true):
    if not Y_aprox:
        return 0

    errores = [1 if punto not in Y_true else 0 for punto in Y_aprox]
    metrica_error = sum(errores) / len(Y_aprox)

    return metrica_error


Ytrue = mejor_frente

