
import cursos
import texto
import entregas

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests

from collections import namedtuple
import os



URL_ACTIVIDADES = 'https://eminus.uv.mx/eminus/actividades/centroActividades.aspx'
URL_ACTIVIDADES_ALUMNOS = 'https://eminus.uv.mx/eminus/Evaluacion/IntegrantesActividades.aspx'
URL_ACTIVIDAD_DETALLE = 'https://eminus.uv.mx/eminus/actividades/RevisionActividad.aspx'
URL_DESCARGA_RESPUESTA = 'https://eminus.uv.mx/eminus/Recursos.aspx?id=%s&tipo=1'

Enlace = namedtuple('Enlace', 'nombre url')

def ir_a_actividades(driver):
    entregas.ir_a_entregas(driver, cursos.URL_MAIN, 'tileActividades', URL_ACTIVIDADES)
    

def regresar_actividades(driver):
    assert driver.current_url == URL_ACTIVIDADES
    i = 0
    while True:
        # necesario para evitar referencias stale
        actividades = driver.find_elements_by_class_name('slActividad')
        if i >= len(actividades):
            break
        yield actividades[i]
        i += 1

def get_nombre_actividad(actividad):
    return actividad.find_element_by_class_name('reltop25').get_attribute("textContent").strip()


def ver_actividades(actividades):
    salida = ''
    for actividad in actividades.values():
        salida += '\n' + get_nombre_actividad(actividad)
    return salida

def ir_a_actividad(driver, actividad):
    assert driver.current_url == URL_ACTIVIDADES
    nombre = get_nombre_actividad(actividad)
    actividad.find_element_by_class_name('reltop25').click()
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, 'lblNombreActividad'), nombre))
    except:
        raise Exception('No se puede acceder a la actividad solicitada')
    

def regresar_alumnos_contestaron_actividad(driver):
    """
    Regresa un generador con los elemenentos asociados a alumnos que contestaron a la actividad
    Tiene acoplamiento semantico con extraer_respuestas_actividad
    Necesita que despues de cada yield se regrese a la pagina URL_ACTIVIDADES_ALUMNOS
    Probablemente sea la forma mas eficiente de implementar
    """
    assert driver.current_url == URL_ACTIVIDADES_ALUMNOS
    i = 0
    rehacer_lookup = True
    while True:
        # Es necesario hacerlo asi para evitar referencias stale
        if rehacer_lookup:
            alumnos = driver.find_elements_by_class_name('DivContenedorDatos')
        if i >= len(alumnos):
            break
        rehacer_lookup = False
        if not 'rgb(0, 0, 51)' in alumnos[i].find_element_by_tag_name('label').get_attribute("style"):
            yield alumnos[i].get_attribute('id'), alumnos[i]
            rehacer_lookup = True
            
        i += 1
        

def ir_a_respuesta_alumno(driver, alumno):
    assert driver.current_url == URL_ACTIVIDADES_ALUMNOS
    alumno.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'contenedorIntegranteEnc')))
    except:
        raise Exception('No se pudo acceder al detalle de la actividad del alumno')
    

def regresar_texto_respuesta_alumno(driver):
    assert driver.current_url == URL_ACTIVIDAD_DETALLE
    html = driver.find_element_by_id('dvRedaccion').get_attribute('innerHTML')
    txt = texto.prettyfy(html) 
    return txt

def regresar_enlaces_archivos_respuesta_alumno(driver):
    assert driver.current_url == URL_ACTIVIDAD_DETALLE
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
    

def guardar_actividad_alumno(driver, texto, enlaces, ruta_salida):
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

def crear_descripcion_actividad(driver, ruta_salida):
    driver.current_url == URL_ACTIVIDADES_ALUMNOS
    descripcion = driver.find_element_by_id('__contenedorDescrip')
    txt = texto.prettyfy(descripcion.get_attribute('innerHTML'))
    with open('%s/%s' % (ruta_salida, 'descripcion.txt'), 'w') as archivo:
        archivo.write(txt)
    
def extraer_respuestas_actividad(driver, actividad, ruta_salida):
    """
    Guarda todos los recursos de una actividad creando una estructura de directorios en ruta
    """
    assert driver.current_url == URL_ACTIVIDADES
    ir_a_actividad(driver, actividad)
    crear_descripcion_actividad(driver, ruta_salida)
    for matricula, alumno in regresar_alumnos_contestaron_actividad(driver):
        ruta_alumno = crear_ruta(ruta_salida, matricula)
        ir_a_respuesta_alumno(driver, alumno)
        texto = regresar_texto_respuesta_alumno(driver)
        enlaces = regresar_enlaces_archivos_respuesta_alumno(driver)
        guardar_actividad_alumno(driver, texto, enlaces, ruta_alumno)
        driver.back()
        driver.refresh()
        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, 'EtiquetaTitulo1'), 'Actividad'))
        except:
            raise Exception('No se puede acceder a la actividad solicitada')

def extraer_respuestas_actividades_curso(driver, ruta_salida):
    """
    Realiza una extraccion de todas las respuestas de todas las actividades de un curso
    """
    assert driver.current_url == URL_ACTIVIDADES
    index = 1
    for actividad in regresar_actividades(driver):
        nombre = str(index) + '.- ' + get_nombre_actividad(actividad)
        ruta_actividad = crear_ruta(ruta_salida, nombre)        
        extraer_respuestas_actividad(driver, actividad, ruta_actividad)
        driver.back()
        driver.refresh()
        index += 1
        try:
            WebDriverWait(driver, 10).until(
                lambda browser: browser.current_url == URL_ACTIVIDADES)
        except:
            raise Exception('No se pudo tener acceso a las actividades')
