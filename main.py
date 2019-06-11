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

    ac.extraer_respuestas_actividad(driver, actividades, 'contenedor-504270', '/tmp/nuevo')
    
    #print(ac.ver_actividades(actividades))
    #ac.ir_a_actividad(driver, actividades, 'contenedor-504270')
    #print(driver.current_url)
    #alumnos_actividad = ac.regresar_alumnos_contestaron_actividad(driver)
    #ac.ir_a_respuesta_alumno(driver, 'zS16013665', alumnos_actividad)
    #print(driver.current_url)
    #texto = ac.regresar_texto_respuesta_alumno(driver)
    #enlaces = ac.regresar_enlaces_archivos_respuesta_alumno(driver)
    #ac.guardar_actividad_alumno(driver, texto, enlaces, '/tmp/test')
    
    #ir_a_cursos_terminados(driver)
    #print(driver.current_url)
    #terminados = regresar_cursos(driver)
    #print(ver_cursos(terminados))
