import login 
import cursos as cr
import actividades as ac
import os

if __name__ == '__main__':            
    driver = login.configure()
    login.login(driver, os.environ.get('user'), os.environ.get('pass'))
    cursos = cr.regresar_cursos(driver)
    print(cr.ver_cursos(cursos))
    cr.ir_a_curso(driver, cursos, '94368')
    ac.ir_a_actividades(driver)

    ac.extraer_respuestas_actividades_curso(driver, '/tmp/actividades')
    

