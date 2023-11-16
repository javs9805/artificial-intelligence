import json

# Lee el archivo JSON
with open('pareto_optimo.json', 'r') as file:
    frentes_pareto_data = json.load(file)

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
