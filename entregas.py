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
