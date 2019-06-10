
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

URL_LOGIN = 'https://eminus.uv.mx/eminus/default.aspx'
URL_MAIN = 'https://eminus.uv.mx/eminus/PrincipalEminus.aspx'
URL_ACTIVIDADES = 'https://eminus.uv.mx/eminus/actividades/centroActividades.aspx'
URL_ACTIVIDADES_ALUMNOS = 'https://eminus.uv.mx/eminus/Evaluacion/IntegrantesActividades.aspx'

def configure():
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/chromium'
    options.add_argument('headless')
    options.add_argument('window-size=1800x1024')
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def login(driver, user, pwd):
    driver.get(URL_LOGIN)    
    assert 'Eminus' in driver.title
    usuario = driver.find_element_by_id('usuario')
    password = driver.find_element_by_id('pass')
    submit = driver.find_element_by_id('boton_logueo')
    usuario.send_keys(user)
    password.send_keys(pwd)
    submit.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, 'lblTotalCursos'), 'Mostrando'))
        time.sleep(1)
    except Exception as err:
        print(err)
        driver.close()
        raise Exception('No se pudo realizar el login')

def ciclar_cursos_hasta(driver, etiqueta):
    tipo_listado = driver.find_element_by_id('lbltipoCurso')
    if not tipo_listado.text == etiqueta:
        izquierda = driver.find_element_by_id('flechaIzq')
        while not tipo_listado.text == etiqueta:
            anterior = tipo_listado.text
            izquierda.click()
            try:
                WebDriverWait(driver, 10).until(
                    lambda useless: anterior != tipo_listado.text)
            except Exception as err:
                raise Exception('No se pudo ciclar los tipos de cursos')

def ciclar_cursos_hasta_vigentes(driver):
    ciclar_cursos_hasta(driver, 'Cursos vigentes')

def ciclar_cursos_hasta_terminados(driver):
    ciclar_cursos_hasta(driver, 'Cursos terminados')
            
def ir_a_cursos_vigentes(driver):
    if not driver.current_url == URL_MAIN:
        driver.get(URL_MAIN)
        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, 'lblTotalCursos'), 'Mostrando'))
            time.sleep(1)
        except Exception as err:
            raise Exception('No se pudo regresar a los cursos vigentes')
    else:
        ciclar_cursos_hasta_vigentes()

def ir_a_cursos_terminados(driver):
    if not driver.current_url == URL_MAIN:
        ir_a_cursos_vigentes(driver)

    ciclar_cursos_hasta_terminados(driver)
            
        
def regresar_cursos(driver):
    assert driver.current_url == URL_MAIN
    vigentes = driver.find_elements_by_class_name('contenedorCurso')
    resultado = {}
    for curso in vigentes:
        resultado[curso.get_attribute('id')] = curso
    return resultado

def ver_cursos(cursos):
    salida = ''
    for curso in cursos.values():
        # no se usa directo text porque no muestra hidden
        salida += '\n' + curso.find_element_by_class_name('AreaTitulo').get_attribute("textContent")
    return salida

def esta_seleccionado_curso(curso):
    return not 'white' in curso.get_attribute("style")

def get_curso_seleccionado(driver, cursos):
    if not driver.current_url == URL_MAIN:
        return None
    for pk in cursos.keys():
        if esta_seleccionado_curso(cursos[pk]):
            return pk

def ir_a_curso(driver, cursos, pk):
    seleccionado = get_curso_seleccionado(driver, cursos)
    if pk == seleccionado:
        return
    if not pk in cursos.keys():
        raise Exception('ID de curso no encontrado')
    assert driver.current_url == URL_MAIN
    cursos[pk].click()
    try:
        WebDriverWait(driver, 10).until(
            lambda useless : esta_seleccionado_curso(cursos[pk]))
    except Exception as err:
        raise Exception('No se pudo tener acceso al curso')
    
def ir_a_actividades(driver):
    assert driver.current_url == URL_MAIN
    tile_actividades = driver.find_element_by_id('tileActividades')
    tile_actividades.click()
    try:
        WebDriverWait(driver, 10).until_not(
            lambda browser: browser.current_url == URL_MAIN)
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
    

def regresar_alumnos_contestaron_actividad(driver, actividades):
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
    pass

def regresar_texto_respuesta_alumno(driver):
    pass

def guardar_archivos_respuesta_alumno(driver, ruta):
    pass

def extraer_respuestas_actividad(driver, actividades, pk, ruta):
    """
    Guarda todos los recursos de una actividad creando una estructura de directorios en ruta
    """

# aquí continua todo lo de la sección de evaluación
    
if __name__ == '__main__':            
    driver = configure()
    login(driver, os.environ.get('user'), os.environ.get('pass'))
    cursos = regresar_cursos(driver)
    print(ver_cursos(cursos))
    ir_a_curso(driver, cursos, '94368')
    ir_a_actividades(driver)
    print(driver.current_url)
    actividades = regresar_actividades(driver) 
    print(ver_actividades(actividades))
    ir_a_actividad(driver, actividades, 'contenedor-491260')
    print(driver.current_url)
    alumnos_actividad = regresar_alumnos_contestaron_actividad(driver, actividades)
    
    #ir_a_cursos_terminados(driver)
    #print(driver.current_url)
    #terminados = regresar_cursos(driver)
    #print(ver_cursos(terminados))
