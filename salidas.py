"""
Módulo para encapsular la forma en que se manipulan salidas
de información en la aplicación
"""

import config

def imprimir_salida(texto, nivel=0):
    for i in range(nivel):
        print('  ', end='')
    print(texto, file=config.salida)


