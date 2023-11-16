import random

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

# Ejemplo de uso
poblacion_actual = [...]  # Tu población de individuos
dummy_fitness_con_sharing = [...]  # Tu lista de valores de dummy fitness

# Seleccionar padres mediante torneo binario
padre1 = binary_tournament_selection(poblacion_actual, dummy_fitness_con_sharing)
padre2 = binary_tournament_selection(poblacion_actual, dummy_fitness_con_sharing)

# Los padres seleccionados son padre1 y padre2
