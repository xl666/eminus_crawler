import excepciones

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

URL_MAIN = 'https://eminus.uv.mx/eminus/PrincipalEminus.aspx'

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
            except:
                raise excepciones.CursosException('No se pudo ciclar los tipos de cursos')

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
            raise excepciones.CursosException('No se pudo regresar a los cursos vigentes')
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
    except:
        raise excepciones.CursosException('No se pudo tener acceso al curso')
