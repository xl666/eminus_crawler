#!/usr/bin/env python3

import os
import sys
import getopt
import getpass

import login 
import cursos as cr
import evaluaciones as ev
import actividades as ac
import config
import excepciones
import cifrado

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
SALT = 'x_39'

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

def guardar_credenciales(mensaje):
    try:
        with open('%s/%s' % (BASE_DIR, 'credenciales.cif'), 'wb') as archivo:
            archivo.write(mensaje)
    except:
        raise excepciones.CredencialesException('No se pudo crear archivo de credenciales en %s/%s' % (BASE_DIR, 'credenciales.cif'))

def crear_credenciales():
    usuario = input('Usuario eminus: ')
    password1 = getpass.getpass('Contraseña eminus: ')
    password2 = getpass.getpass('Repetir contraseña eminus: ')
    pw1 = getpass.getpass('Frase para recuperar credenciales: ')
    pw2 = getpass.getpass('Repetir frase: ')
    if password1 != password2 or pw1 != pw2:
        raise excepciones.CredencialesException('Los passwords no concuerdan')
    if ':' in usuario or ':' in password1:
        raise excepciones.CredencialesException('No se puede usar el caracter :')
    mensaje = cifrado.cifrar('%s:%s' % (usuario, password1), pw1, SALT)
    guardar_credenciales(mensaje)

def recuperar_credenciales():
    try:
        with open('%s/%s' % (BASE_DIR, 'credenciales.cif'), 'rb') as archivo:
            contenido = archivo.read()
            password = getpass.getpass('Frase para recuperar credenciales: ')
            mensaje = cifrado.descifrar(contenido, password, SALT)
            mensaje = mensaje.decode('utf-8')
            usuario, pw = mensaje.split(':')
            return usuario, pw
    except Exception as err:
        print(err)
        raise excepciones.CredencialesException('No se encontró el archivo credenciales.cif')


def listar_cursos(terminados=False):
    driver = config.configure()
    usuario, password = recuperar_credenciales()
    login.login(driver, usuario, password)
    if terminados:
        cr.ir_a_cursos_terminados(driver)
    cursos = cr.regresar_cursos(driver)
    print(cr.ver_cursos(cursos))
    
def extraer_evidencias(terminados):
    driver = config.configure()
    usuario, password = recuperar_credenciales()
    login.login(driver, usuario, password)
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

    if opcionL:            
        listar_cursos(terminados)
        exit(0)

    if opcionE:
        extraer_evidencias(terminados)
        exit(0)

    if opcionC:
        crear_credenciales()
