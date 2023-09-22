from A_START_F1 import iniciarSolucion as funcionAStarF1
from A_START_F2 import iniciarSolucion as funcionAStarF2
from BFS import iniciarSolucion as funcionBFS
import eel
import json
# Inicializa la aplicación Eel y configura la carpeta web
eel.init("front")

# Define rutas y funciones de la aplicación web
@eel.expose
def AstarUno(matriz,N):
    #matriz = [[1,2,3],[4,0,5],[7,8,6]]
    print(matriz)
    print(N)
    solucion = funcionAStarF1(matriz,N)
    listEstados = []
    solucion.reverse()
    for s in solucion:
        listEstados.append(s.state)
    return json.dumps(listEstados)

@eel.expose
def AstarDos(matriz,N):
    #matriz = [[1,2,3],[4,0,5],[7,8,6]]
    print(matriz)
    print(N)
    solucion = funcionAStarF2(matriz,N)
    listEstados = []
    solucion.reverse()
    for s in solucion:
        listEstados.append(s.state)
    return json.dumps(listEstados)

@eel.expose
def bfs(matriz,N):
    print(matriz)
    print(N)
    solucion = funcionBFS(matriz,N)
    listEstados = []
    solucion.reverse()
    for s in solucion:
        listEstados.append(s.state)
    return json.dumps(listEstados)
# Inicia la aplicación web
eel.start("index.html")


