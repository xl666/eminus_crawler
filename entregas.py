"""
Modulo para extraer todo lo que tienen en comun las actividades y las evaluaciones
"""

def ir_a_entregas(driver, urlCurrent, idTitulo, urlNext):
    assert driver.current_url == urlCurrent
    tile = driver.find_element_by_id(idTitulo)
    tile.click()
    try:
        WebDriverWait(driver, 10).until(
            lambda browser: browser.current_url == urlNext)
    except:
        raise Exception('No se pudo tener acceso al elemento')
