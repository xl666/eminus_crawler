#!/usr/bin/env python3

import login 
import cursos as cr
import evaluaciones as ev
import actividades as ac
import os
import config
import sys
import getopt

def listar_cursos(driver, terminados=False):    
    if terminados:
        cr.ir_a_cursos_terminados(driver)
    cursos = cr.regresar_cursos(driver)
    print(cr.ver_cursos(cursos))

def modo_uso():
    print('eminus_extractor.py [OPCIONES]')
    print('Opciones:')
    print('    -h, --help: ver esta ayuda')
    print('    -c, --credenciales: establecer credenciales en modo interactivo')
    print('    -n, --navegador: establecer configuración de navegador a usar en modo interactivo')
    print('    -l, --listar: listar cursos (por defecto vigentes) mostrando ids')
    print('    -t, --terminados: activar modo cursos terminados (por defecto se usan vigentes)')
    print('    -d valor, --directorio=valor: opcional, directorio de salida (debe existir), por defecto directorio actual')
    print('    -e valor, --evidencias=valor: lista de ids de cursos a extraer evidencias')
    print('       se sigue el formato id1,id2,...,idn  sin espacios')
    print('')
    print('Ejemplos de uso:')
    print('')
    print('Configurar credenciales:')
    print('    eminus_extractor -c')
    print('')
    print('Listar cursos terminados:')
    print('    eminus_extractor -l -t')
    print('')
    print('Extraer evidencias de un curso vigente:')
    print('    eminus_extractor -e 1000 -d /tmp/evidencias')
    print('')
    print('Extraer evidencias de tres cursos terminados:')
    print('    eminus_extractor -e 1000,2000,3000 -t -d /tmp/evidencias')

def validar_ids(cadena):
    partes = cadena.split(',')
    for elemento in partes:
        if not elemento.isnumeric():
            return False
    return True

def validar_combinaciones(opcionC, opcionN, opcionL, opcionE, opcionD):
    if opcionC and True in (opcionN, opcionL, opcionE, opcionD):
        return False
    if opcionN and True in (opcionC, opcionL, opcionE, opcionD):
        return False
    if opcionL and True in (opcionC, opcionN, opcionE, opcionD):
        return False
    
    return True

def extraer_evidencias(driver, terminados):
    cursos = cr.regresar_cursos(driver)
    cr.extraer_evidencias_lista_cursos(driver, cursos, evidencias, directorio, terminados)
    
if __name__ == '__main__':

    if len(sys.argv) < 2:
        modo_uso()
        exit(0)
    
    options, remainder = getopt.getopt(sys.argv[1:], 'hcnltd:e:', ['help', 'credenciales', 'navegador', 'listar', 'terminados', 'directorio=', 'evidencias='])

    if remainder:
        modo_uso()
    
    terminados = False
    directorio = '.'
    evidencias = []

    opcionL = False
    opcionD = False
    opcionE = False
    opcionC = False
    opcionN = False
    
    for opcion, valor in options:
        if opcion in ('-h', '--help'):
            modo_uso()
            exit(0)
        if opcion in ('-c', '--credenciales'):
            opcionC = True
        if opcion in ('-n', '--navegador'):
            opcionN = True
        if opcion in ('-l', '--listar'):
            opcionL = True
        if opcion in ('-t', '--terminados'):
            terminados = True
        if opcion in ('-d', '--directorio'):
            if not os.path.isdir(valor):
                print('%s no es un directorio válido' % valor)
                exit(1)
            opcionD = True
            directorio = valor
        if opcion in ('-e', '--evidencias'):
            if not validar_ids(valor):
                print('Los ids deben ser números enteros separados por coma, sin espacios')
                exit(1)
            opcionE = True
            evidencias = valor.split(',')

    if not validar_combinaciones(opcionC, opcionN, opcionL, opcionE, opcionD):
        modo_uso()
        exit(1)

            
    driver = config.configure()
    login.login(driver, os.environ.get('user'), os.environ.get('pass'))

    if opcionL:            
        listar_cursos(driver, terminados)
        exit(0)

    if opcionE:
        extraer_evidencias(driver, terminados)
        exit(0)
    
    #cr.ir_a_cursos_terminados(driver)
    #cursos = cr.regresar_cursos(driver)
    #print(cr.ver_cursos(cursos))
    #cr.extraer_evidencias_lista_cursos(driver, cursos, ['78671','84723'], '/tmp/evidencias', True)
    #cr.extraer_evidencias_curso(driver, cursos, '94369', '/tmp/cibercrimen')
    #cr.ir_a_curso(driver, cursos, '94368')
    #ev.ir_a_evaluaciones(driver)
    #ev.extraer_respuestas_evaluaciones_curso(driver, '/tmp/evaluaciones')
    
    #ac.ir_a_actividades(driver)
    #ac.extraer_respuestas_actividades_curso(driver, '/tmp/actividades')
    

