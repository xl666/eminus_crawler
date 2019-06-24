"""
Modulo para extraer todo lo que tienen en comun las actividades y las evaluaciones
"""


import cursos
import texto

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests

from collections import namedtuple
import os

URL_DESCARGA_RESPUESTA = 'https://eminus.uv.mx/eminus/Recursos.aspx?id=%s&tipo=1'

Enlace = namedtuple('Enlace', 'nombre url')

def ir_a_entregas(driver, urlCurrent, idTitulo, urlNext):
    assert driver.current_url == urlCurrent
    tile = driver.find_element_by_id(idTitulo)
    tile.click()
    try:
        WebDriverWait(driver, 10).until(
            lambda browser: browser.current_url == urlNext)
    except:
        raise Exception('No se pudo tener acceso al elemento')

def regresar_entregas(driver, urlCurrent, cssClassEntrega):
    assert driver.current_url == urlCurrent
    i = 0
    while True:
        # necesario para evitar referencias stale
        entregas = driver.find_elements_by_class_name(cssClassEntrega)
        if i >= len(entregas):
            break
        yield entregas[i]
        i += 1

def get_nombre_entrega(driver, entrega, urlCurrent):
    assert driver.current_url == urlCurrent
    return entrega.find_element_by_class_name('reltop25').get_attribute("textContent").strip()

def ver_entregas(driver, entregas, urlCurrent):
    assert driver.current_url == urlCurrent
    salida = ''
    for entrega in entregas:
        salida += '\n' + get_nombre_entrega(driver, entrega, urlCurrent)
    return salida

def ir_a_entrega(driver, entrega, urlCurrent):
    assert driver.current_url == urlCurrent
    nombre = get_nombre_entrega(driver, entrega, urlCurrent)
    entrega.find_element_by_class_name('reltop25').click()
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, 'lblNombreActividad'), nombre))
    except:
        raise Exception('No se puede acceder a la entrega solicitada')


def alumno_contesto_entrega(alumno):
    test1 = not 'rgb(0, 0, 51)' in alumno.find_element_by_tag_name('label').get_attribute("style")
    test2 = alumno.find_element_by_xpath('following::label').get_attribute("textContent").strip() != '-'
    if test1 or test2:
        return True
    return False
    
    
def regresar_alumnos_contestaron_entrega(driver, urlCurrent):
    """
    Regresa un generador con los elemenentos asociados a alumnos que contestaron a la entrega
    Tiene acoplamiento semantico con extraer_respuestas_entrega
    Necesita que despues de cada yield se regrese a la pagina de entregas 
    Probablemente sea la forma mas eficiente de implementar
    """
    assert driver.current_url == urlCurrent
    i = 0
    rehacer_lookup = True
    while True:
        # Es necesario hacerlo asi para evitar referencias stale
        if rehacer_lookup:
            alumnos = driver.find_elements_by_class_name('DivContenedorDatos')
        if i >= len(alumnos):
            break
        rehacer_lookup = False
        if alumno_contesto_entrega(alumnos[i]):
            yield alumnos[i].get_attribute('id'), alumnos[i]
            rehacer_lookup = True
        i += 1

def ir_a_respuesta_alumno(driver, alumno, urlCurrent):
    assert driver.current_url == urlCurrent
    alumno.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'contenedorIntegranteEnc')))
    except:
        raise Exception('No se pudo acceder al detalle de la entrega del alumno')


def regresar_texto_respuesta_alumno(driver, urlCurrent):
    assert driver.current_url == urlCurrent
    html = driver.find_element_by_id('dvRedaccion').get_attribute('innerHTML')
    txt = texto.prettyfy(html) 
    return txt

def regresar_enlaces_archivos_respuesta_alumno(driver, urlCurrent):
    assert driver.current_url == urlCurrent
    enlaces = []
    try:
        entrega = driver.find_element_by_id('sctMaterialEstudiante')
    except:
        return []
    descargas = entrega.find_elements_by_class_name('filaArchivoDescarga')
    nombres = entrega.find_elements_by_class_name('filaArchivoNombre')
    for info in zip(nombres, descargas):
        # el formato se ve como: descargarArchivo(1,2680088,2)
        detalles = info[1].get_attribute('onclick').split(',')
        enlaces.append(Enlace(info[0].get_attribute("textContent"),
                              URL_DESCARGA_RESPUESTA % detalles[1]))        
    return enlaces

def guardar_enlace(driver, enlace, ruta):
    nombre, url = enlace
    all_cookies = driver.get_cookies()
    cookies = {}  
    for s_cookie in all_cookies:
        cookies[s_cookie["name"]] = s_cookie["value"]
    
    respuesta = requests.get(url, cookies=cookies)
    with open('%s/%s' % (ruta, nombre), 'wb') as archivo:
        archivo.write(respuesta.content)
    

def guardar_entrega_alumno(driver, texto, enlaces, ruta_salida, urlCurrent):
    assert driver.current_url == urlCurrent
    if texto.strip():
        with open('%s/%s' % (ruta_salida, 'texto_resputesta.txt'), 'w') as archivo:
            archivo.write(texto)

    for enlace in enlaces:
        guardar_enlace(driver, enlace, ruta_salida)
    
def crear_ruta(ruta_base, sub_dir):
    ruta = '%s/%s' % (ruta_base, sub_dir)
    try:            
        os.mkdir(ruta)
        return ruta
    except FileExistsError:
        if not os.path.isdir(ruta):
            raise Exception('No se puede crear directorio para guardar archivos de alumno, la ruta ya existe y no es directorio:%s' % ruta)
    except Exception:
        raise Exception('No se puede crear directorio para guardar archivos de alumno')

def crear_descripcion_entrega(driver, ruta_salida, urlCurrent):
    driver.current_url == urlCurrent
    descripcion = driver.find_element_by_id('__contenedorDescrip')
    txt = texto.prettyfy(descripcion.get_attribute('innerHTML'))
    with open('%s/%s' % (ruta_salida, 'descripcion.txt'), 'w') as archivo:
        archivo.write(txt)

def extraer_respuestas_entrega(driver, entrega, ruta_salida, urlCurrent, urlStep2, urlStep3, etiqueta):
    """
    Guarda todos los recursos de una entrega creando una estructura de directorios en ruta
    """
    assert driver.current_url == urlCurrent
    ir_a_entrega(driver, entrega, urlCurrent)
    crear_descripcion_entrega(driver, ruta_salida, urlStep2)
    for matricula, alumno in regresar_alumnos_contestaron_entrega(driver, urlStep2):
        ruta_alumno = crear_ruta(ruta_salida, matricula)
        ir_a_respuesta_alumno(driver, alumno, urlStep2)
        texto = regresar_texto_respuesta_alumno(driver, urlStep3)
        enlaces = regresar_enlaces_archivos_respuesta_alumno(driver, urlStep3)
        guardar_entrega_alumno(driver, texto, enlaces, ruta_alumno, urlStep3)
        driver.back()
        driver.refresh()
        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, 'EtiquetaTitulo1'), etiqueta))
        except:
            raise Exception('No se puede acceder a la entrega solicitada')


def extraer_respuestas_entregas_curso(driver, ruta_salida, urlCurrent, urlStep2, urlStep3, etiqueta, cssClassEntrega):
    """
    Realiza una extraccion de todas las respuestas de todas las entregas de un curso
    """
    assert driver.current_url == urlCurrent
    index = 1
    for actividad in regresar_entregas(driver, urlCurrent, cssClassEntrega):
        nombre = str(index) + '.- ' + get_nombre_entrega(driver, actividad, urlCurrent)
        ruta_entrega = crear_ruta(ruta_salida, nombre)
        extraer_respuestas_entrega(driver, actividad, ruta_entrega, urlCurrent, urlStep2, urlStep3, etiqueta)
        driver.back()
        driver.refresh()
        index += 1
        try:
            WebDriverWait(driver, 10).until(
                lambda browser: browser.current_url == urlCurrent)
        except:
            raise Exception('No se pudo tener acceso a las entregas')