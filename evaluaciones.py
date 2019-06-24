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
URL_EVALUACION_DETALLE = 'https://eminus.uv.mx/eminus/Evaluacion/RevisionEvaluacion.aspx' 

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

def ir_a_respuesta_alumno(driver, alumno):
    entregas.ir_a_respuesta_alumno(driver, alumno, URL_EVALUACIONES_ALUMNOS)

def regresar_texto_respuesta_alumno(driver):
    return entregas.regresar_texto_respuesta_alumno(driver, URL_EVALUACION_DETALLE)

def regresar_enlaces_archivos_respuesta_alumno(driver):
    return entregas.regresar_enlaces_archivos_respuesta_alumno(driver, URL_EVALUACION_DETALLE)

def crear_descripcion_evaluacion(driver, ruta_salida):
    entregas.crear_descripcion_entrega(driver, ruta_salida, URL_EVALUACIONES_ALUMNOS)
