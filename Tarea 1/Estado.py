class Estado:
    objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    evaluacion_greedy = None
    evaluacion_AStar = None
    heuristica = None

    def __init__(self, estado, padre, direccion, profundidad, costo):
        self.estado = estado
        self.padre = padre
        self.direccion = direccion
        self.profundidad = profundidad

        if padre:
            self.costo = padre.costo + costo
        else:
            self.costo = costo

    def prueba(self):
        if self.estado == self.objetivo:
            return True
        return False

    def Distancia_Manhattan(self, n):
        self.heuristica = 0
        for i in range(1, n * n):
            distancia = abs(self.estado.index(i) - self.objetivo.index(i))
            self.heuristica = self.heuristica + distancia / n + distancia % n

        self.evaluacion_greedy = self.heuristica
        self.evaluacion_AStar = self.heuristica + self.costo

        return (self.evaluacion_greedy, self.evaluacion_AStar)

    def Fichas_Descolocadas(self, n):
        contador = 0
        self.heuristica = 0
        for i in range(n * n):
            for j in range(n * n):
                if self.estado[i] != self.objetivo[j]:
                    contador += 1
                self.heuristica = self.heuristica + contador

        self.evaluacion_greedy = self.heuristica
        self.evaluacion_AStar = self.heuristica + self.costo

        return (self.evaluacion_greedy, self.evaluacion_AStar)

    @staticmethod
    def movimientos_disponibles(x, n):
        movimientos = ['Izquierda', 'Derecha', 'Arriba', 'Abajo']
        if x % n == 0:
            movimientos.remove('Izquierda')
        if x % n == n - 1:
            movimientos.remove('Derecha')
        if x - n < 0:
            movimientos.remove('Arriba')
        if x + n > n * n - 1:
            movimientos.remove('Abajo')

        return movimientos

    def expandir(self, n):
        x = self.estado.index(0)
        movimientos = self.movimientos_disponibles(x, n)

        hijos = []
        for direccion in movimientos:
            temp = self.estado.copy()
            if direccion == 'Izquierda':
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direccion == 'Derecha':
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direccion == 'Arriba':
                temp[x], temp[x - n] = temp[x - n], temp[x]
            elif direccion == 'Abajo':
                temp[x], temp[x + n] = temp[x + n], temp[x]

            hijos.append(Estado(temp, self, direccion, self.profundidad + 1, 1))  # La profundidad debe cambiarse a medida que se producen los hijos
        return hijos

    def solucion(self):
        solucion = []
        solucion.append(self.direccion)
        path = self
        while path.padre is not None:
            path = path.padre
            solucion.append(path.direccion)
        solucion = solucion[:-1]
        solucion.reverse()
        return solucion
