
import cursos
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

URL_ACTIVIDADES = 'https://eminus.uv.mx/eminus/actividades/centroActividades.aspx'
URL_ACTIVIDADES_ALUMNOS = 'https://eminus.uv.mx/eminus/Evaluacion/IntegrantesActividades.aspx'
URL_ACTIVIDAD_DETALLE = 'https://eminus.uv.mx/eminus/actividades/RevisionActividad.aspx'
URL_DESCARGA_RESPUESTA = 'https://eminus.uv.mx/eminus/Recursos.aspx?id=%s&tipo=1'

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
    Regresa los elemenentos asociados a alumnos que contestaron a la actividad
    el diccionario de retorno es matricula: elemento
    """
    assert driver.current_url == URL_ACTIVIDADES_ALUMNOS
    alumnos = driver.find_elements_by_class_name('DivContenedorDatos')
    respuesta = {}
    for alumno in alumnos:
        if not 'rgb(0, 0, 51)' in alumno.find_element_by_tag_name('label').get_attribute("style"):
            respuesta[alumno.get_attribute('id')] = alumno
    return respuesta

def ir_a_respuesta_alumno(driver, matricula, alumnos):
    assert driver.current_url == URL_ACTIVIDADES_ALUMNOS
    alumnos.get(matricula).click()
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
    entrega = driver.find_element_by_id('sctMaterialEstudiante')
    descargas = entrega.find_elements_by_class_name('filaArchivoDescarga')
    nombres = entrega.find_elements_by_class_name('filaArchivoNombre')
    for info in zip(nombres, descargas):
        # el formato se ve como: descargarArchivo(1,2680088,2)
        detalles = info[1].get_attribute('onclick').split(',')
        enlaces.append((info[0].get_attribute("textContent"),
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
    pass
