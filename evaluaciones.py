import cursos
import texto
import entregas

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

from collections import namedtuple
import os

URL_EVALUACIONES = 'https://eminus.uv.mx/eminus/Evaluacion/CentroEvaluacion.aspx'
URL_EVALUACIONES_ALUMNOS = 'https://eminus.uv.mx/eminus/Evaluacion/IntegrantesActividades.aspx'

def ir_a_evaluaciones(driver):
    entregas.ir_a_entregas(driver, cursos.URL_MAIN, 'tileInfoContacto', URL_EVALUACIONES)

def regresar_evaluaciones(driver):
    return entregas.regresar_entregas(driver, URL_EVALUACIONES, 'slEvaluacion')

def get_nombre_evaluacion(driver, evaluacion):
    return entregas.get_nombre_entrega(driver, evaluacion, URL_EVALUACIONES)

def ver_evaluaciones(driver, evaluaciones):
    return entregas.ver_entregas(driver, evaluaciones, URL_EVALUACIONES)

def ir_a_evaluacion(driver, evaluacion):
    entregas.ir_a_entrega(driver, evaluacion, URL_EVALUACIONES)

def regresar_alumnos_contestaron_evaluacion(driver):
    return entregas.regresar_alumnos_contestaron_entrega(driver, URL_EVALUACIONES_ALUMNOS)
