
import excepciones

import requests


def crear_ruta(ruta_base, sub_dir):
    ruta = '%s/%s' % (ruta_base, sub_dir)
    try:            
        os.mkdir(ruta)
        return ruta
    except FileExistsError:
        if not os.path.isdir(ruta):
            raise excepciones.RutaException('No se puede crear directorio para guardar archivos de alumno, la ruta ya existe y no es directorio:%s' % ruta)
        raise excepciones.RutaException('No se puede crear directorio %s, ya existe' % ruta)
    except Exception:
        raise excepciones.RutaException('No se puede crear directorio para guardar archivos de alumno')


def guardar_archivo(path, contenido):
    try:
        with open(path, 'w') as archivo:
            archivo.write(contenido)
    except:
        raise excepciones.RutaException('Hubo un problema al guardar %s' % path)
    
def guardar_enlace(driver, enlace, ruta):
    nombre, url = enlace
    all_cookies = driver.get_cookies()
    cookies = {}  
    for s_cookie in all_cookies:
        cookies[s_cookie["name"]] = s_cookie["value"]
    
    respuesta = requests.get(url, cookies=cookies)
    with open('%s/%s' % (ruta, nombre), 'wb') as archivo:
        archivo.write(respuesta.content)
