import numpy as np
import pandas as pd
from FileReader import FileReader
import random


class M3AS:
    
    def __init__(self, num_nodes, num_ants, t0, beta, rho,  f01, f02, distancia):
        self.num_nodes = num_nodes
        self.num_ants = num_ants
        self.tau = np.full((num_nodes, num_nodes), t0)  # Pheromone matrix
        self.rho = rho      # Pheromone evaporation rate
        self.f01 = f01      # Objective function 1 matrix
        self.f02 = f02      # Objective function 2 matrix
        self.distancia = distancia  # Distance matrix
        self.beta = beta
        self.lamda1 = 0
        self.beta = 0
        self.lamda2 = 0


   
    
    


archivo_objetivo1 = 'qapUni.75.0.1.qap.txt'
archivo_objetivo2 = 'qapUni.75.p75.1.qap.txt'


reader_objetivo1 = FileReader(archivo_objetivo1)
reader_objetivo1.leer_matriz_de_adyacencia()

objetivo1 = reader_objetivo1.obtener_objetivo1()
objetivo2 = reader_objetivo1.obtener_objetivo2()
distancias = reader_objetivo1.obtener_distancias()
cantidad_localidades = reader_objetivo1.obtener_cantidad_localidades()
    

num_nodes = 5
num_ants = 3
t0 = 0.1
beta = 2.0
rho = 0.5
w = 10





def seleccion_por_torneos_probabilista(node_list, tabla_feromonas, heta_1, heta_2, lamda1, lamda2, beta):
    indices_no_visitados = [i for i, visited in node_list if not visited]

    k = np.random.randint(1, len(indices_no_visitados) + 1)
    participantes = np.random.choice(indices_no_visitados, size=k, replace=False)
    
    indice_ganador = max(participantes, key=lambda i: calcular_puntaje(i, tabla_feromonas, heta_1, heta_2, lamda, beta))
    
    node_list[indice_ganador] = (node_list[indice_ganador][0], True)  # Marcar como visitado
    
    return indice_ganador




def get_nodo_con_mayor_probabilidad(node_list, tabla_feromonas, heta_1, heta_2, lamda1, lamda2, beta):
    indices_no_visitados = [i for i, visited in node_list if not visited]
    participantes = indices_no_visitados
    indice_ganador = max(participantes, key=lambda i: calcular_puntaje(i, tabla_feromonas, heta_1, heta_2, lamda, beta))
    
    node_list[indice_ganador] = (node_list[indice_ganador][0], True)  # Marcar como visitado
    
    return indice_ganador

# Definir el valor de Q
Q = 0.7

def pseudo_random_rule(source_nodes, lamda1, lamda2, beta, q, probabilidad_matriz, tau, heta1, heta2):
    q0 = random.random()
    if q0 <= Q:
        nodo = seleccion_por_torneos_probabilista(source_nodes, heta1, heta2, lamda, beta)
        return nodo
        print("A")
    else:
        #seleccionar el nodo con mayor probabilidad
        nodo = get_nodo_con_mayor_probabilidad(source_nodes, tau , heta1, heta2, lamda, beta)
        return nodo
        print("B")

def calcular_asignacion_de_costo(node_i, node_j,distancia,flujo):     
    return distancia[node_i][node_j]*flujo[node_i][node_j]    

def calcular_probabilidad(Ni):
    probabilidad = [[0 for _ in range(m3as_instance.num_nodes)] for _ in range(m3as_instance.num_nodes)]
    for i in range(0,m3as_instance.num_nodes):
        sum = 0
        for g in range(0,m3as_instance.num_nodes):
            if g in Ni:
                sum = m3as_instance.tau[i][g]*(())**m3as_instance.beta




def calcular_probabilidad_de_Ni(node_i,Ni):
    Ni_list = list(Ni)
    costo1_Ni = list(Ni)
    costo2_Ni= list(Ni)
    
    for idx in range(0,Ni_list):
        node_j = Ni_list[idx]
        costo1_Ni[idx] = calcular_asignacion_de_costo(node_i,node_j,m3as_instance.distancia, m3as_instance.f01)
        costo2_Ni[idx] = calcular_asignacion_de_costo(node_i, node_j,m3as_instance.distancia,m3as_instance.f02)


    
def construir_arbol(source_nodes):
    T = set()
    R = source_nodes
    Ni = source_nodes
    while R:
        #Quitar un elemento de R
        nodo_i =  R.pop()
        #Construir el conjunto N
        Ni = Ni.remove(nodo_i)
        if len(Ni) !=0:
            p_Ni = list(Ni)







# Crear la lista de tuplas

m3as_instance = M3AS(num_nodes, num_ants, t0, beta, rho, objetivo1, objetivo2, cantidad_localidades)    
initial_boolean_value = True  
print(m3as_instance.tau)


for generacion in range(1,100):
    for lamda1 in range(1,num_ants-1):
        for lamda2 in range(1, num_ants -1):
            source_nodes = set(range(cantidad_localidades))
            m3as_instance.lamda1 = lamda1
            m3as_instance.lamda2 = lamda2

          #para buscar las soluciones se debe seguir la regla de transicion
            print("Waiting")  
