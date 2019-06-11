
import cursos
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from collections import namedtuple
import os
import copy


URL_ACTIVIDADES = 'https://eminus.uv.mx/eminus/actividades/centroActividades.aspx'
URL_ACTIVIDADES_ALUMNOS = 'https://eminus.uv.mx/eminus/Evaluacion/IntegrantesActividades.aspx'
URL_ACTIVIDAD_DETALLE = 'https://eminus.uv.mx/eminus/actividades/RevisionActividad.aspx'
URL_DESCARGA_RESPUESTA = 'https://eminus.uv.mx/eminus/Recursos.aspx?id=%s&tipo=1'

Enlace = namedtuple('Enlace', 'nombre url')

def ir_a_actividades(driver):
    assert driver.current_url == cursos.URL_MAIN
    tile_actividades = driver.find_element_by_id('tileActividades')
    tile_actividades.click()
    try:
        WebDriverWait(driver, 10).until_not(
            lambda browser: browser.current_url == cursos.URL_MAIN)
    except:
        raise Exception('No se pudo tener acceso a las actividades')

def regresar_actividades(driver):
    assert driver.current_url == URL_ACTIVIDADES
    actividades = driver.find_elements_by_class_name('slActividad')
    resultado = {}
    for actividad in actividades:
        resultado[actividad.get_attribute('id')] = actividad
    return resultado

def get_nombre_actividad(actividad):
    return actividad.find_element_by_class_name('reltop25').get_attribute("textContent").strip()


def ver_actividades(actividades):
    salida = ''
    for actividad in actividades.values():
        salida += '\n' + get_nombre_actividad(actividad)
    return salida

def ir_a_actividad(driver, actividades, pk):
    if not pk in actividades.keys():
        raise Exception('La actividad no existe')
    assert driver.current_url == URL_ACTIVIDADES
    nombre = get_nombre_actividad(actividades[pk])
    actividades[pk].find_element_by_class_name('reltop25').click()
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
    respuesta = {}
    i = 0
    while True:
        # Es necesario hacerlo asi para evitar referencias stale
        alumnos = driver.find_elements_by_class_name('DivContenedorDatos')
        if i >= len(alumnos):
            break
        if not 'rgb(0, 0, 51)' in alumnos[i].find_element_by_tag_name('label').get_attribute("style"):
            yield alumnos[i].get_attribute('id'), alumnos[i]
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
    texto = driver.find_element_by_id('dvRedaccion').get_attribute("textContent").strip()
    return texto

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
    

def extraer_respuestas_actividad(driver, actividades, pk, ruta_salida):
    """
    Guarda todos los recursos de una actividad creando una estructura de directorios en ruta
    """
    assert driver.current_url == URL_ACTIVIDADES
    ir_a_actividad(driver, actividades, pk)
    for matricula, alumno in regresar_alumnos_contestaron_actividad(driver):
        ruta_alumno = '%s/%s' % (ruta_salida, matricula)
        try:            
            os.mkdir(ruta_alumno)
        except FileExistsError:
            if not os.path.isdir(ruta_alumno):
                raise Exception('No se puede crear directorio para guardar archivos de alumno, la ruta ya existe y no es directorio:%s' % ruta_alumno)
        except Exception:
            raise Exception('No se puede crear directorio para guardar archivos de alumno')
            
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
