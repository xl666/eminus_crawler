
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

URL_LOGIN = 'https://eminus.uv.mx/eminus/default.aspx'


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
    

