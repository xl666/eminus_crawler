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

def ir_a_evaluaciones(driver):
    entregas.ir_a_entregas(driver, cursos.URL_MAIN, 'tileInfoContacto', URL_EVALUACIONES)
