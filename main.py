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
    print(driver.current_url)
    actividades = ac.regresar_actividades(driver) 
    print(ac.ver_actividades(actividades))
    ac.ir_a_actividad(driver, actividades, 'contenedor-491260')
    print(driver.current_url)
    alumnos_actividad = ac.regresar_alumnos_contestaron_actividad(driver, actividades)
    
    #ir_a_cursos_terminados(driver)
    #print(driver.current_url)
    #terminados = regresar_cursos(driver)
    #print(ver_cursos(terminados))
