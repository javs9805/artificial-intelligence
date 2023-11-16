import subprocess

# Ruta al archivo .py que quieres ejecutar
archivo_py = 'test3.py'

# Número de veces que quieres ejecutar el código
veces_a_correr = 50

for _ in range(veces_a_correr):
    # Utiliza subprocess para ejecutar el archivo .py en un nuevo proceso
    subprocess.run(['python', archivo_py])
