class FileReader:
    def __init__(self, archivo):
        self.archivo = archivo
        self.objetivo1 = None
        self.objetivo2 = None
        self.distancias = None
        self.cantidad_localidades = None

    def leer_matriz_de_adyacencia(self):
        with open(self.archivo, 'r') as f:
            self.cantidad_localidades = int(f.readline().strip())
            self.objetivo1 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(self.cantidad_localidades)]
            f.readline()  # Leer línea en blanco
            self.objetivo2 = [[int(valor) for valor in f.readline().strip().split()] for _ in range(self.cantidad_localidades)]
            f.readline()  # Leer línea en blanco
            self.distancias = [[int(valor) for valor in f.readline().strip().split()] for _ in range(self.cantidad_localidades)]

    def obtener_objetivo1(self):
        return self.objetivo1

    def obtener_objetivo2(self):
        return self.objetivo2

    def obtener_distancias(self):
        return self.distancias

    def obtener_cantidad_localidades(self):
        return self.cantidad_localidades

# Ejemplo de uso:
archivo_objetivo1 = 'qapUni.75.0.1.qap.txt'
archivo_objetivo2 = 'qapUni.75.p75.1.qap.txt'

reader_objetivo1 = FileReader(archivo_objetivo1)
reader_objetivo1.leer_matriz_de_adyacencia()

objetivo1 = reader_objetivo1.obtener_objetivo1()
objetivo2 = reader_objetivo1.obtener_objetivo2()
distancias = reader_objetivo1.obtener_distancias()
cantidad_localidades = reader_objetivo1.obtener_cantidad_localidades()
